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
        
        # Создаем категорию по умолчанию, если её нет
        default_category = Category.query.filter_by(name='Общее').first()
        if not default_category:
            default_category = Category(name='Общее')
            db.session.add(default_category)
            db.session.commit()
            print("Created default category")
        
        # Создаем администратора, если его нет
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print("Created admin user")
        
        print('База данных инициализирована')

if __name__ == '__main__':
    init_db() 