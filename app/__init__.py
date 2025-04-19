from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

    from app.routes import auth_routes, material_routes, moderation_routes, search_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(material_routes.bp)
    app.register_blueprint(moderation_routes.bp)
    app.register_blueprint(search_routes.bp)

    return app 