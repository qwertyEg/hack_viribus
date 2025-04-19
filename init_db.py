from app import create_app, db
from app.models.user import User
from app.models.category import Category
from app.models.material import Material

def init_db():
    app = create_app()
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        
        # Создаем тестовые категории, если их нет
        if Category.query.count() == 0:
            categories = [
                Category(name='Математика'),
                Category(name='Физика'),
                Category(name='Химия'),
                Category(name='Биология'),
                Category(name='История'),
                Category(name='Литература'),
                Category(name='Иностранные языки'),
                Category(name='Программирование'),
                Category(name='Искусство'),
                Category(name='Другое')
            ]
            for category in categories:
                db.session.add(category)
            db.session.commit()
            print('Категории созданы')
        
        # Создаем администратора, если его нет
        if User.query.filter_by(username='admin').first() is None:
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print('Администратор создан')
        
        print('База данных инициализирована')

if __name__ == '__main__':
    init_db() 