import os
import sys

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User

def check_user(username):
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            print(f"Пользователь {username} найден. Текущая роль: {user.role}")
        else:
            print(f"Пользователь {username} не найден в базе данных")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Использование: python check_user.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    check_user(username) 