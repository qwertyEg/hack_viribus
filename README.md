# Техническое задание для образовательного веб-сервиса и Telegram-бота

# Детальная структура проекта и тестов

## Окончательная структура проекта
```
project_root/
│
├── app/
│   ├── __init__.py             # Инициализация Flask, SQLAlchemy, LoginManager
│   ├── config.py               # Конфигурация приложения (SECRET_KEY, SQLALCHEMY_DATABASE_URI)
│   │
│   ├── models/
│   │   ├── user.py             # Модель User: id, username, role, materials, ratings
│   │   ├── material.py         # Модель Material: id, title, description, file_url, status
│   │   ├── rating.py           # Модель Rating: id, user_id, material_id, value
│   │   └── category.py         # Модель Category: id, name, materials
│   │
│   ├── routes/
│   │   ├── auth_routes.py      # /login, /register, /logout
│   │   ├── material_routes.py  # /upload, /materials/<id>, /rate
│   │   ├── moderation_routes.py# /moderation, /approve/<id>, /delete/<id>
│   │   └── search_routes.py    # /search?query=...&category=...
│   │
│   ├── forms/
│   │   ├── login_form.py       # Форма: username, password, remember
│   │   ├── upload_form.py      # Форма: title, description, category, file
│   │   └── rating_form.py      # Форма: rating_value (1-5)
│   │
│   ├── services/
│   │   ├── auth_service.py     # register_user(), check_credentials()
│   │   ├── drive_service.py    # upload_file(), delete_file()
│   │   └── moderation_service.py # get_pending_materials()
│   │
│   ├── templates/
│   │   ├── base.html           # Базовый шаблон с навигацией
│   │   ├── auth/
│   │   │   ├── login.html      # Форма входа
│   │   │   └── register.html   # Форма регистрации
│   │   ├── materials/
│   │   │   ├── upload.html     # Форма загрузки + валидация файлов
│   │   │   ├── details.html    # Просмотр материала + рейтинг
│   │   │   └── list.html       # Список материалов с фильтрами
│   │   └── moderation/
│   │       └── panel.html      # Таблица материалов на модерацию
│   │
│   └── static/
│       ├── css/
│       │   └── main.css        # Стили для всех страниц
│       └── js/
│           └── rating.js       # AJAX-обработка оценок
│
├── tests/
│   ├── conftest.py             # Фикстуры для тестов
│   ├── test_models.py          # Тесты моделей БД
│   ├── test_routes.py          # Тесты эндпоинтов
│   └── test_services.py        # Тесты бизнес-логики
│
├── migrations/                 # Автогенерируемые миграции
├── requirements.txt            # Зависимости: Flask, SQLAlchemy, pytest и др.
└── .env                        # Переменные окружения (опционально)
```

## Подробное описание ключевых файлов

### 1. Модели (`models/`)
```python
# user.py
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')  # user/moderator/admin
    materials = db.relationship('Material', backref='author', lazy=True)
```

```python
# material.py
class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    file_url = db.Column(db.String(500))  # Ссылка на Google Drive
    status = db.Column(db.String(20), default='unapproved')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    ratings = db.relationship('Rating', backref='material', lazy='dynamic')
```

### 2. Роуты (`routes/`)
```python
# material_routes.py
@materials_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        try:
            file_url = DriveService.upload_file(form.file.data)
            material = Material(
                title=form.title.data,
                file_url=file_url,
                author_id=current_user.id
            )
            db.session.add(material)
            db.session.commit()
            flash('Материал успешно загружен! Ожидайте модерации', 'success')
        except DriveAPIError:
            flash('Ошибка загрузки файла', 'danger')
    return render_template('materials/upload.html', form=form)
```

### 3. Тесты (`tests/`)
```python
# test_models.py
def test_create_material(app):
    with app.app_context():
        user = User(username='test_user')
        material = Material(title='Test', author=user)
        db.session.add_all([user, material])
        db.session.commit()
        assert material.status == 'unapproved'
        assert material in user.materials

# test_routes.py
def test_upload_unauthorized(client):
    response = client.get('/upload', follow_redirects=True)
    assert b'Login required' in response.data

def test_moderation_access(client, moderator_user):
    client.login_user(moderator_user)
    response = client.get('/moderation')
    assert response.status_code == 200
```

## Пошаговая реализация тестов

### 1. Тестирование моделей (`test_models.py`)
- Создание пользователей с разными ролями
- Проверка связей (1 пользователь → N материалов)
- Тестирование статусов материалов
- Проверка расчетов среднего рейтинга

### 2. Тестирование роутов (`test_routes.py`)
- Неавторизованный доступ к защищенным страницам
- Успешная загрузка файла с моком Google Drive
- Проверка прав модератора/администратора
- Тестирование поиска с разными параметрами

### 3. Тестирование сервисов (`test_services.py`)
- Мокирование Google Drive API
- Тестирование регистрации с дубликатами username
- Проверка фильтрации материалов по статусу

## Инструкция по запуску тестов
```bash
# Установите тестовые зависимости
pip install pytest pytest-mock

# Запуск всех тестов
pytest -v tests/

# Запуск конкретного модуля
pytest -v tests/test_routes.py

# Генерация coverage-отчета
pytest --cov=app --cov-report=html
```

## Советы по реализации
1. Для Google Drive API используйте `unittest.mock` для мокирования:
```python
from unittest.mock import MagicMock

def test_drive_upload(mocker):
    mock_service = MagicMock()
    mocker.patch('services.drive_service.build', return_value=mock_service)
    
    result = DriveService.upload_file(b'test_content')
    assert result.startswith('https://drive.google.com')
```

2. Для тестирования авторизации используйте `Flask-Login`:
```python
def test_admin_panel_access(client):
    # Создаем обычного пользователя
    user = User(username='user', role='user')
    
    # Пытаемся войти как обычный пользователь
    client.login_user(user)
    
    # Пытаемся получить доступ к админ-панели
    response = client.get('/admin')
    assert response.status_code == 403
```

3. Используйте фикстуры для повторяющихся данных:
```python
# conftest.py
@pytest.fixture
def test_client(app):
    return app.test_client()

@pytest.fixture
def sample_material(app):
    with app.app_context():
        user = User(username='author')
        material = Material(title='Sample', author=user)
        db.session.add_all([user, material])
        db.session.commit()
        return material.id
``` 

Эта структура обеспечит:
- Четкое разделение компонентов
- Легкое добавление новых функций
- Простое тестирование всех слоев приложения
- Возможность масштабирования до production-окружения