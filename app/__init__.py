from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from app.config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Увеличиваем максимальный размер загружаемого файла до 16MB
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    # Создаем директории для загрузки и скачивания файлов
    os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static', 'downloads'), exist_ok=True)
    
    # Создаем директорию instance, если она не существует
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Устанавливаем путь к базе данных
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'app.db')}"
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

    from app.routes import auth_routes, material_routes, moderation_routes, search_routes, home_routes, chat_routes
    app.register_blueprint(home_routes.bp)
    app.register_blueprint(chat_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(material_routes.bp)
    app.register_blueprint(moderation_routes.bp)
    app.register_blueprint(search_routes.bp)

    return app 