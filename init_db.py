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
            # Математика
            Material(
                title='Введение в математический анализ',
                description='Базовые понятия математического анализа, включая пределы, производные и интегралы',
                file_url='https://drive.google.com/file/d/1',
                status='approved',
                author_id=1,
                category_id=1
            ),
            Material(
                title='Линейная алгебра',
                description='Основы линейной алгебры: матрицы, определители, системы линейных уравнений',
                file_url='https://drive.google.com/file/d/2',
                status='approved',
                author_id=1,
                category_id=1
            ),
            Material(
                title='Теория вероятностей',
                description='Основные понятия теории вероятностей и математической статистики',
                file_url='https://drive.google.com/file/d/3',
                status='approved',
                author_id=1,
                category_id=1
            ),
            Material(
                title='Дифференциальные уравнения',
                description='Решение обыкновенных дифференциальных уравнений различных типов',
                file_url='https://drive.google.com/file/d/4',
                status='approved',
                author_id=1,
                category_id=1
            ),
            Material(
                title='Математическая статистика',
                description='Методы математической статистики и их применение в анализе данных',
                file_url='https://drive.google.com/file/d/5',
                status='approved',
                author_id=1,
                category_id=1
            ),
            Material(
                title='Комплексный анализ',
                description='Функции комплексного переменного, интегралы и ряды в комплексной плоскости',
                file_url='https://drive.google.com/file/d/6',
                status='approved',
                author_id=1,
                category_id=1
            ),
            # Физика
            Material(
                title='Основы квантовой механики',
                description='Введение в квантовую механику и её основные принципы',
                file_url='https://drive.google.com/file/d/7',
                status='approved',
                author_id=1,
                category_id=2
            ),
            Material(
                title='Классическая механика',
                description='Законы Ньютона, законы сохранения, колебания и волны',
                file_url='https://drive.google.com/file/d/8',
                status='approved',
                author_id=1,
                category_id=2
            ),
            Material(
                title='Термодинамика',
                description='Основные законы термодинамики и их применение',
                file_url='https://drive.google.com/file/d/9',
                status='approved',
                author_id=1,
                category_id=2
            ),
            Material(
                title='Электродинамика',
                description='Электричество и магнетизм, уравнения Максвелла',
                file_url='https://drive.google.com/file/d/10',
                status='approved',
                author_id=1,
                category_id=2
            ),
            # Химия
            Material(
                title='Общая химия',
                description='Основные понятия и законы химии, строение атома',
                file_url='https://drive.google.com/file/d/11',
                status='approved',
                author_id=1,
                category_id=3
            ),
            Material(
                title='Органическая химия',
                description='Строение и свойства органических соединений',
                file_url='https://drive.google.com/file/d/12',
                status='approved',
                author_id=1,
                category_id=3
            ),
            Material(
                title='Физическая химия',
                description='Химическая термодинамика и кинетика',
                file_url='https://drive.google.com/file/d/13',
                status='approved',
                author_id=1,
                category_id=3
            ),
            # Биология
            Material(
                title='Общая биология',
                description='Основы биологии, клеточная теория, генетика',
                file_url='https://drive.google.com/file/d/14',
                status='approved',
                author_id=1,
                category_id=4
            ),
            Material(
                title='Анатомия человека',
                description='Строение и функции органов и систем человека',
                file_url='https://drive.google.com/file/d/15',
                status='approved',
                author_id=1,
                category_id=4
            ),
            Material(
                title='Экология',
                description='Взаимодействие организмов с окружающей средой',
                file_url='https://drive.google.com/file/d/16',
                status='approved',
                author_id=1,
                category_id=4
            ),
            # История
            Material(
                title='История Древнего мира',
                description='Цивилизации Древнего Востока, Греции и Рима',
                file_url='https://drive.google.com/file/d/17',
                status='approved',
                author_id=1,
                category_id=5
            ),
            Material(
                title='История Средних веков',
                description='Европа в период Средневековья',
                file_url='https://drive.google.com/file/d/18',
                status='approved',
                author_id=1,
                category_id=5
            ),
            Material(
                title='История Нового времени',
                description='Европа в XVI-XIX веках',
                file_url='https://drive.google.com/file/d/19',
                status='approved',
                author_id=1,
                category_id=5
            ),
            Material(
                title='История России',
                description='Основные этапы развития Российского государства',
                file_url='https://drive.google.com/file/d/20',
                status='approved',
                author_id=1,
                category_id=5
            )
        ]
        
        for material in materials:
            db.session.add(material)
        
        db.session.commit()
        print('Database initialized with test data!')

if __name__ == '__main__':
    init_db() 