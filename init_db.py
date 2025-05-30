from app import create_app, db
from app.models.user import User
from app.models.category import Category
from app.models.material import Material

def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create test categories
        categories = [
            Category(name='Математика'),
            Category(name='Физика'),
            Category(name='Химия'),
            Category(name='Биология'),
            Category(name='История')
        ]
        
        for category in categories:
            db.session.add(category)
        
        # Create admin user
        admin = User(username='admin', role='admin')
        admin.set_password('admin')
        db.session.add(admin)
        
        # Create test materials
        materials = [
            Material(
                title='Введение в математический анализ',
                description='Базовые понятия математического анализа',
                file_url='https://drive.google.com/file/d/1',
                status='approved',
                author_id=1,
                category_id=1
            ),
            Material(
                title='Основы квантовой механики',
                description='Введение в квантовую механику',
                file_url='https://drive.google.com/file/d/2',
                status='approved',
                author_id=1,
                category_id=2
            )
        ]
        
        for material in materials:
            db.session.add(material)
        
        db.session.commit()
        print('Database initialized with test data!')

if __name__ == '__main__':
    init_db() 