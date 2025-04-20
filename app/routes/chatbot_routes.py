from flask import Blueprint, request, jsonify, render_template, current_app
from flask_login import login_required, current_user
import logging

logger = logging.getLogger(__name__)

chatbot_bp = Blueprint('chatbot', __name__)

# Инициализация чат-бота будет происходить при первом запросе
_chatbot = None

def get_chatbot():
    global _chatbot
    if _chatbot is None:
        try:
            from src.chat_bot import ChatBot
            logger.info("Инициализация чат-бота")
            _chatbot = ChatBot()
            logger.info("Чат-бот успешно инициализирован")
        except Exception as e:
            logger.error(f"Ошибка при инициализации чат-бота: {str(e)}")
            raise
    return _chatbot

@chatbot_bp.route('/')
@login_required
def chat():
    return render_template('chat/chat.html')

@chatbot_bp.route('/ask', methods=['POST'])
@login_required
def ask():
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
            
        logger.info(f"Получен запрос: {query}")
            
        # Получаем ответ от чат-бота
        try:
            chatbot = get_chatbot()
            response = chatbot.ask(query)
            
            logger.info(f"Получен ответ от чат-бота: {response}")
            
            return jsonify({
                'success': True,
                'response': response['answer'],
                'needs_clarification': False
            })
            
        except Exception as e:
            logger.error(f"Error in chatbot: {str(e)}", exc_info=True)
            return jsonify({
                'success': False,
                'error': f'Error from chatbot: {str(e)}'
            }), 500
            
    except Exception as e:
        logger.error(f"Error in route: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 