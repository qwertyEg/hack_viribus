import os
import sys

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User

def make_moderator(username):
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            user.role = 'moderator'
            db.session.commit()
            print(f"Пользователь {username} успешно назначен модератором")
        else:
            print(f"Пользователь {username} не найден")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Использование: python make_moderator.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    make_moderator(username) 