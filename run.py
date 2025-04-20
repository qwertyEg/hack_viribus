from app import create_app, db
import os

app = create_app()

if __name__ == '__main__':
    # Проверяем, существует ли база данных
    db_path = os.path.join(app.instance_path, 'app.db')
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
    
    # Запускаем приложение с отключенным режимом отладки
    app.run(debug=False, host='0.0.0.0', port=5003) 