# Техническое задание для образовательного веб-сервиса и Telegram-бота

## 1. Общее описание
**Цель**: Создать платформу для хранения и поиска учебных материалов с интеграцией Telegram-бота и ИИ-помощника.  
**Целевая аудитория**: Студенты и преподаватели.  
**Стек технологий** (рекомендуемый):
- Бэкенд: Python (FastAPI/Django), PostgreSQL, Redis (кеширование)
- Фронтенд: React.js/Vue.js (опционально)
- Telegram-бот: aiogram
- ИИ-модуль: OpenAI API/Hugging Face
- Хостинг: Docker, Nginx, AWS/Heroku

---

## 2. Функциональные требования

### 2.1 Веб-сервис
#### 2.1.1 Авторизация и регистрация
- Регистрация через email или социальные сети (Google, GitHub)
- Ролевая модель: пользователь, модератор, администратор
- Восстановление пароля

#### 2.1.2 Управление материалами
- Загрузка файлов (PDF, MP4, DOCX) с метаданными: 
  - Название, описание, теги, категория (лекция/семинар/задачник и т.д.), предмет (матан, линал)
- Система категорий:
  - Иерархия: Предмет → Подкатегория (напр., "Матан 1") → Тип материала (лекция)
- Модерация контента (для модераторов)

#### 2.1.3 Поиск и фильтрация
- Поиск по: названию, тегам, описанию, содержимому (для текстов)
- Фильтры: 
  - Рейтинг (от 1 до 5 звезд)
  - Тип материала
  - Дата загрузки
  - Предмет

#### 2.1.4 Рейтинговая система
- Оценка материалов пользователями (1-5 звезд)
- Расчет среднего рейтинга с учетом веса оценок
- Топ-10 материалов на главной странице

#### 2.1.5 Профиль пользователя
- История загрузок/просмотров
- Возможность создавать персональные коллекции материалов

---

### 2.2 Telegram-бот
#### 2.2.1 Авторизация
- Привязка аккаунта через веб-сервис (OAuth2)
- Сессия с JWT-токеном

#### 2.2.2 Основное меню
- **Поиск**: Глобальный поиск по всем материалам (интеграция с API веб-сервиса)
- **Библиотека**: 
  - Разделы: Семинары, Лекции, Учебники и т.д.
  - Просмотр материалов с пагинацией
- **Предметы**: 
  - Древовидное меню: Предмет → Подкатегория → Список материалов
- **Помощник**: 
  - Чат с ИИ для составления учебного плана (пример запроса: "Посоветуй материалы по матану за 1 семестр")
  - Сохранение рекомендаций в профиле

#### 2.2.3 Оценка материалов
- Кнопки "Оценить" после просмотра материала
- Рейтинг влияет на позицию в поиске

---

## 3. API-спецификация (ключевые методы)
### 3.1 Материалы
- `POST /api/materials` – загрузка материала (требуется роль модератора)
- `GET /api/materials?search=...&category=...` – поиск
- `POST /api/materials/{id}/rate` – оценка материала

### 3.2 Пользователи
- `POST /api/auth/login` – авторизация
- `GET /api/users/me` – данные профиля

### 3.3 ИИ-помощник
- `POST /api/ai/assist` – обработка запросов пользователя (возвращает текстовый ответ + список рекомендованных материалов)

---

## 4. Интерфейсы
### 4.1 Веб-сервис
- Главная страница: поисковая строка, топ материалов, категории
- Страница материала: плеер/просмотрщик файлов, кнопка оценки, метаданные
- Личный кабинет: история активности, настройки

### 4.2 Telegram-бот
- Интерактивное меню с кнопками
- Прелоадер при загрузке материалов
- Уведомления о новых материалах по подписке

---

## 5. Безопасность
- HTTPS для всех запросов
- Валидация файлов (макс. размер: 500 МБ, разрешенные типы: pdf, mp4, docx)
- Защита от XSS и SQL-инъекций
- Rate-limiting для API (100 запросов/мин)

---

## 6. Развертывание
- Контейнеризация (Docker)
- Настройка CI/CD (GitHub Actions)
- Резервное копирование БД (ежедневно)

---

## 7. Тестирование
- Unit-тесты для API (pytest)
- Интеграционные тесты бота (behave)
- Нагрузочное тестирование (Locust)

---

## 8. Документация
- Swagger/OpenAPI для веб-сервиса
- Инструкция по запуску (README.md)
- Архитектурная схема (draw.io)

---

## 9. Лицензия
- MIT License

---

# Детали реализации веб-сервиса

## Стек технологий
- **Фреймворк**: FastAPI (для API) + ASGI-сервер (Uvicorn)
- **База данных**: PostgreSQL + SQLAlchemy (ORM)
- **Миграции**: Alembic
- **Кеширование**: Redis
- **Асинхронные задачи**: Celery (для обработки файлов/видео)
- **Аутентификация**: JWT (JSON Web Tokens)
- **Файловое хранилище**: Amazon S3 / MinIO (локально)
- **Дополнительно**: 
  - Pydantic (валидация данных)
  - python-multipart (загрузка файлов)
  - Pillow (обработка изображений-превью)
  - Elasticsearch (опционально для расширенного поиска)

---

## Структура проекта (Python)

```
edu-platform/
├── docker-compose.yml          # Конфигурация Docker
├── Dockerfile                  # Сборка образа
├── .env                        # Переменные окружения
├── requirements.txt            # Зависимости
│
├── src/                        # Основной код
│   ├── core/                   # Базовые настройки
│   │   ├── config.py           # Конфигурация приложения
│   │   ├── database.py         # Подключение к БД
│   │   └── security.py         # Логика JWT
│   │
│   ├── apps/                   # Модули приложения
│   │   ├── auth/               # Аутентификация
│   │   │   ├── routers.py      # API-эндпоинты
│   │   │   ├── schemas.py      Pydantic-схемы
│   │   │   ├── services.py     Бизнес-логика
│   │   │   └── models.py       SQLAlchemy-модели
│   │   │
│   │   ├── materials/          # Управление материалами
│   │   │   ├── routers.py
│   │   │   ├── schemas.py
│   │   │   ├── services.py
│   │   │   └── models.py
│   │   │
│   │   ├── ai/                 # ИИ-помощник
│   │   │   ├── routers.py
│   │   │   └── services.py
│   │   │
│   │   └── search/             # Поисковая система
│   │       ├── services.py
│   │       └── models.py
│   │
│   ├── migrations/             # Миграции Alembic
│   ├── static/                 # Статика (превью, файлы)
│   ├── tasks/                  # Celery-задачи
│   │   └── process_file.py     # Обработка видео/документов
│   │
│   ├── main.py                 # Точка входа
│   └── utils/                  # Вспомогательные модули
│       ├── file_upload.py      # Логика загрузки файлов
│       └── pagination.py       # Пагинация запросов
│
├── tests/                      # Тесты
│   ├── test_api.py             # API-тесты
│   └── conftest.py             # Фикстуры
│
└── celery/                     # Конфиг Celery
    └── worker.py               # Запуск воркера
```

---

## Описание ключевых компонентов

### 1. Модуль `auth`
- **Регистрация**: 
  - Валидация email через регулярные выражения
  - Хеширование паролей (bcrypt)
  - Отправка подтверждения на email (Celery-таска)
- **Авторизация**:
  - Генерация JWT-токена (access + refresh)
  - Middleware для проверки токенов

### 2. Модуль `materials`
- **Загрузка файлов**:
  - Проверка MIME-типа и размера
  - Генерация превью для видео (Celery + FFmpeg)
  - Сохранение метаданных в БД
  - Интеграция с S3/MinIO
- **Иерархия категорий**:
  ```python
  class Category(BaseModel):
      id: int
      name: str
      parent_id: Optional[int]  # Для вложенности (Предмет → Подкатегория)
  ```

### 3. Поисковая система
- **Реализация**:
  - Базовый поиск: PostgreSQL Full-Text Search
  - Расширенный поиск (опционально): Elasticsearch
- **Фильтрация**:
  ```python
  class MaterialFilter(BaseModel):
      rating__gte: Optional[float]
      category_id: Optional[int]
      type: Optional[MaterialType]  # enum: Лекция/Семинар и т.д.
  ```

### 4. ИИ-модуль
- **Интеграция**:
  - Запросы к OpenAI API / локальной модели
  - Парсинг учебных запросов (например: "Материалы по матану за 2 курс")
  - Контекстный поиск в БД по ключевым словам
- **Пример ответа**:
  ```json
  {
    "text": "Рекомендую эти материалы...",
    "materials": [{"id": 1, "title": "Лекция 1"}, ...]
  }
  ```

---

## Пример кода (FastAPI)

### Эндпоинт загрузки материала
```python
# materials/routers.py
from fastapi import APIRouter, Depends, UploadFile
from .schemas import MaterialCreate
from .services import upload_material_service

router = APIRouter()

@router.post("/materials/")
async def upload_material(
    file: UploadFile,
    data: MaterialCreate = Depends(),
    user: User = Depends(get_current_user),
):
    return await upload_material_service(file, data, user)
```

### Сервис обработки файла
```python
# materials/services.py
async def upload_material_service(file: UploadFile, data: MaterialCreate, user: User):
    # Валидация файла
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(400, "Invalid file type")
    
    # Сохранение в S3
    file_url = await s3_upload(file)
    
    # Создание записи в БД
    material = await Material.create(
        title=data.title,
        description=data.description,
        file_url=file_url,
        category_id=data.category_id,
        user_id=user.id
    )
    
    # Запуск фоновой задачи на обработку
    process_file.delay(material.id)
    
    return material
```

---

## Конфигурация Docker
```yaml
# docker-compose.yml
services:
  web:
    build: .
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: edu_platform
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password

  redis:
    image: redis:7

  celery-worker:
    build: .
    command: celery -A celery.worker worker --loglevel=info
    depends_on:
      - redis
```

---

## Workflow обработки материала
1. Пользователь загружает файл через API
2. Файл сохраняется в S3/MinIO
3. В БД создается запись со статусом "processing"
4. Celery-воркер запускает задачу:
   - Для видео: генерация превью, конвертация в HLS
   - Для PDF: извлечение текста для поиска
   - Для изображений: создание thumbnail
5. Обновление статуса материала на "active"

---

## Тестирование
Пример теста для API:
```python
# tests/test_api.py
async def test_upload_material(authenticated_client):
    file = ("test.pdf", open("test.pdf", "rb"), "application/pdf")
    response = authenticated_client.post(
        "/materials/",
        files={"file": file},
        data={"title": "Test Lecture"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Lecture"
```

---

## как лучше начать
1. Начните с core-модулей (аутентификация, базовый CRUD)
2. Используйте Docker для быстрого развертывания
3. Для MVP можно временно использовать SQLite вместо PostgreSQL
4. Отложите сложные фичи (Elasticsearch, HLS-стриминг) на поздние этапы
5. Используйте готовые решения для ИИ (OpenAI API) вместо локальных моделей



# Детали реализации Telegram-бота с ИИ-интеграцией

## Стек технологий
- **Библиотека**: aiogram 3.x (асинхронная версия)
- **ИИ-модуль**: OpenAI API (GPT-4/3.5-turbo) + кастомные промпты
- **Кеширование**: Redis (для сессий и контекста диалога)
- **Взаимодействие с API**: aiohttp (асинхронные HTTP-запросы)

---

## Структура проекта бота

```
telegram-bot/
├── config/                   # Конфигурация
│   ├── __init__.py
│   └── settings.py           # Токены, API URLs
│
├── handlers/                # Обработчики
│   ├── __init__.py
│   ├── start.py             # Команда /start
│   ├── search.py            # Поиск материалов
│   ├── library.py           # Работа с библиотекой
│   ├── subjects.py          # Навигация по предметам
│   ├── ai_helper.py         # ИИ-помощник
│   └── common.py            # Общие хэндлеры
│
├── keyboards/               # Клавиатуры
│   ├── __init__.py
│   ├── builders.py          # Динамические клавиатуры
│   ├── inline.py            # Inline-кнопки
│   └── reply.py             # Reply-кнопки
│
├── services/                # Логика работы с API и ИИ
│   ├── __init__.py
│   ├── auth.py              # Авторизация через веб-API
│   ├── api_client.py        # Клиент для работы с API
│   ├── ai_processor.py      # Обработчик запросов к ИИ
│   └── rating.py            # Система оценок
│
├── models/                  # Модели данных
│   ├── __init__.py
│   ├── user.py              # Модель пользователя
│   └── materials.py         # Модели материалов
│
├── utils/                   # Вспомогательные модули
│   ├── __init__.py
│   ├── states.py            # FSM состояния
│   └── middleware.py        # Промежуточное ПО
│
└── main.py                  # Точка входа
```

---

## Поэтапная интеграция ИИ

### 1. Настройка клиента для работы с ИИ-API

```python
# services/ai_processor.py
import openai
from config import settings

class AIProcessor:
    def __init__(self):
        openai.api_key = settings.OPENAI_KEY
        self.system_prompt = """
        Ты — помощник для студентов. Анализируй запросы и рекомендую материалы 
        из нашей базы. Формат ответа: 
        1. Краткое пояснение
        2. Список материалов в формате: [ID] Название
        """

    async def generate_response(self, user_query: str, context: list) -> str:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                *context,
                {"role": "user", "content": user_query}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
```

### 2. Интеграция с API веб-сервиса

```python
# services/api_client.py
import aiohttp
from models.materials import Material

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

    async def search_materials(self, query: str, token: str) -> list[Material]:
        headers = {"Authorization": f"Bearer {token}"}
        async with self.session.get(
            f"{self.base_url}/api/materials?search={query}",
            headers=headers
        ) as response:
            return await response.json()

    async def rate_material(self, material_id: int, rating: int, token: str):
        async with self.session.post(
            f"{self.base_url}/api/materials/{material_id}/rate",
            json={"rating": rating},
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            return response.status == 200
```

---

## Реализация ключевых функций

### 1. Авторизация через веб-сервис (OAuth2 Flow)

```python
# handlers/start.py
from aiogram import Router, F
from aiogram.types import Message
from services.auth import AuthService

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    auth_url = AuthService.generate_oauth_url()
    await message.answer(
        "Привет! Для начала работы авторизуйся:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="Войти", url=auth_url)
        ]])
    )
```

### 2. ИИ-помощник с контекстным диалогом

```python
# handlers/ai_helper.py
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from services.ai_processor import AIProcessor
from utils.states import AIHelperState

router = Router()
ai_processor = AIProcessor()

@router.message(F.text == "Помощник")
async def start_ai_helper(message: Message, state: FSMContext):
    await state.set_state(AIHelperState.waiting_query)
    await message.answer("Задай вопрос ИИ-помощнику:")

@router.message(AIHelperState.waiting_query)
async def process_ai_query(message: Message, state: FSMContext):
    context = await state.get_data().get("ai_context", [])
    
    # Получаем ответ от ИИ
    ai_response = await ai_processor.generate_response(
        message.text, 
        context
    )
    
    # Извлекаем ID материалов из ответа
    material_ids = parse_material_ids(ai_response)
    
    # Сохраняем контекст
    await state.update_data(ai_context=[
        *context,
        {"role": "assistant", "content": ai_response}
    ])
    
    # Отправляем ответ с кнопками оценки
    await message.answer(
        ai_response,
        reply_markup=build_rating_keyboard(material_ids)
    )
```

---

## Система оценок материалов

### 1. Клавиатура с кнопками оценки

```python
# keyboards/inline.py
from aiogram.utils.keyboard import InlineKeyboardBuilder

def build_rating_keyboard(material_ids: list[int]):
    builder = InlineKeyboardBuilder()
    for mat_id in material_ids:
        builder.button(
            text=f"Оценить материал #{mat_id}", 
            callback_data=f"rate_{mat_id}")
    return builder.as_markup()
```

### 2. Обработка оценки

```python
# handlers/common.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.rating import RatingService

router = Router()

@router.callback_query(F.data.startswith("rate_"))
async def rate_material(callback: CallbackQuery):
    material_id = int(callback.data.split("_")[1])
    
    # Показываем клавиатуру с оценками 1-5
    await callback.message.answer(
        "Выберите оценку:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data=f"stars_{material_id}_{i}") 
             for i in range(1, 6)]
        ])
    )

@router.callback_query(F.data.startswith("stars_"))
async def process_rating(callback: CallbackQuery):
    _, material_id, rating = callback.data.split("_")
    success = await RatingService.rate_material(
        callback.from_user.id,
        int(material_id),
        int(rating)
    )
    
    await callback.message.answer(
        "✅ Спасибо за оценку!" if success else "❌ Ошибка оценки"
    )
```

---

## Работа с API веб-сервиса

### Пример поиска материалов

```python
# handlers/search.py
from aiogram import Router, F
from aiogram.types import Message
from services.api_client import APIClient

router = Router()
api_client = APIClient("https://api.edu-platform.com")

@router.message(F.text == "Поиск")
async def start_search(message: Message, state: FSMContext):
    await state.set_state(SearchState.waiting_query)
    await message.answer("Введите поисковый запрос:")

@router.message(SearchState.waiting_query)
async def process_search(message: Message, state: FSMContext):
    materials = await api_client.search_materials(
        message.text,
        token=await get_user_token(message.from_user.id)
    
    # Формируем сообщение с пагинацией
    response = "\n".join([f"{m.id}. {m.title}" for m in materials])
    
    await message.answer(
        f"Найдено материалов: {len(materials)}\n{response}",
        reply_markup=build_materials_keyboard(materials)
    )
```

---

## Настройка FSM (Finite State Machine)

```python
# utils/states.py
from aiogram.fsm.state import StatesGroup, State

class SearchState(StatesGroup):
    waiting_query = State()

class AIHelperState(StatesGroup):
    waiting_query = State()

class LibraryState(StatesGroup):
    choosing_category = State()
```

---

## Пример .env файла

```
BOT_TOKEN=your_telegram_token
API_BASE_URL=https://api.edu-platform.com
OPENAI_KEY=sk-...
REDIS_URL=redis://localhost:6379
```

---

## Workflow взаимодействия с ИИ

1. Пользователь активирует помощника через кнопку
2. Бот переходит в состояние ожидания запроса
3. Запрос отправляется в OpenAI API с контекстом:
   - Системный промпт с инструкциями
   - История предыдущих сообщений
4. Ответ ИИ парсится на наличие ID материалов
5. Формируется сообщение с inline-кнопками для оценки
6. Оценка сохраняется через API веб-сервиса

---

## Рекомендации по обучению ИИ

1. Создайте набор примерных диалогов для тонкой настройки:
   ```json
   {
     "messages": [
       {"role": "user", "content": "Нужны материалы по интегралам"},
       {"role": "assistant", "content": "Рекомендую: [123] Лекция по интегралам, [456] Семинар..."}
     ]
   }
   ```

2. Используйте параметры для контроля ответов:
   ```python
   response = await openai.ChatCompletion.acreate(
       ...,
       temperature=0.5,  # Для более детерминированных ответов
       max_tokens=500,
       stop=["\n\n"]      # Ограничение длины
   )
   ```

3. Реализуйте пост-обработку ответов:
   ```python
   def parse_material_ids(text: str) -> list[int]:
       return list(map(int, re.findall(r'\[(\d+)\]', text)))
   ```

---

## Типовая структура сообщения с материалами

```
📚 Найдено 3 материала по запросу "интегралы":

[123] Лекция "Основы интегралов" (Рейтинг: ⭐4.5)
[456] Семинар "Практика интегрирования" 
[789] Учебник "Математический анализ"

Выберите материал для оценки:
```

С кнопками:
- "Оценить материал #123"
- "Оценить материал #456"
- "Оценить материал #789"

---

# Детали реализации Telegram-бота с локальной LLM (Llama 3) (АЛЬТЕРАНТИВНОЕ РЕШЕНИЕ)

## Стек технологий
- **Библиотека**: aiogram 3.x + FastAPI (для локального ИИ-сервиса)
- **LLM**: Llama 3 8B (4-bit квантование через llama.cpp)
- **Инфраструктура**:
  - Ollama (или llama-cpp-python) для работы с моделью
  - Docker + NVIDIA Container Toolkit (для GPU)
  - Redis (кеширование ответов)
- **Оптимизация**: GGUF-формат моделей

---

## Архитектура решения

```
[Пользователь]
  │
  ▼
[Telegram Bot] ↔ [Web Service API] (материалы/рейтинги)
  │
  ▼
[Local LLM Service] (FastAPI + Llama.cpp)
  │
  ▼
[Модель Llama 3 8B] (в Docker-контейнере)
```

---

## Структура проекта (обновленная)

```
llama-edu-bot/
├── docker-compose.yml
├── .env
├── bot/                      # Телеграм-бот
│   ├── handlers/
│   │   └── ai_helper.py      # Обновленный обработчик
│   └── services/
│       └── local_ai.py       # Клиент для локального ИИ
│
├── llama-api/                # Локальный ИИ-сервис
│   ├── app/
│   │   ├── main.py           # FastAPI эндпоинты
│   │   └── model_loader.py   # Загрузка модели
│   ├── models/
│   │   └── llama-3-8b.Q4_K_M.gguf  # Модель в GGUF
│   └── Dockerfile
│
└── docs/
    └── prompts/              # Промпты для обучения
        └── edu-assistant.txt
```

---

## Пошаговая реализация

### 1. Подготовка модели
1. Скачайте GGUF-версию Llama 3 8B:
```bash
wget https://huggingface.co/TheBloke/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf
```
2. Положите файл модели в `llama-api/models/`

### 2. Настройка локального ИИ-сервиса

`llama-api/app/main.py`:
```python
from fastapi import FastAPI
from llama_cpp import Llama
from pydantic import BaseModel

app = FastAPI()
llm = None

class Query(BaseModel):
    prompt: str
    max_tokens: int = 512

@app.on_event("startup")
async def load_model():
    global llm
    llm = Llama(
        model_path="/app/models/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf",
        n_ctx=2048,
        n_gpu_layers=35  # Для GPU
    )

@app.post("/generate")
async def generate_text(query: Query):
    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": query.prompt}],
        max_tokens=query.max_tokens,
        temperature=0.7
    )
    return {"response": response['choices'][0]['message']['content']}
```

`llama-api/Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && pip install llama-cpp-python[server] fastapi uvicorn

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

---

### 3. Обновление docker-compose.yml

```yaml
version: '3.8'

services:
  bot:
    build: ./bot
    environment:
      - AI_API_URL=http://llama-api:8001
    depends_on:
      - llama-api

  llama-api:
    build: ./llama-api
    volumes:
      - ./llama-api/models:/app/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    ports:
      - "8001:8001"

  web-service:
    # Существующая конфигурация веб-сервиса

  redis:
    image: redis:alpine
```

---

### 4. Интеграция с ботом

`bot/services/local_ai.py`:
```python
import aiohttp
from config import settings

class LocalAIClient:
    def __init__(self):
        self.base_url = settings.AI_API_URL
        
    async def generate_edu_response(self, prompt: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/generate",
                json={"prompt": prompt, "max_tokens": 512}
            ) as response:
                data = await response.json()
                return data.get("response", "")
```

`bot/handlers/ai_helper.py` (обновленная версия):
```python
from aiogram import Router, F
from services.local_ai import LocalAIClient

router = Router()
ai_client = LocalAIClient()

@router.message(F.text == "Помощник")
async def handle_ai_request(message: Message):
    # Получаем материалы из API
    materials = await api_client.get_popular_materials()
    
    # Формируем промпт
    prompt = f"""
    [INST]Ты — ассистент курса. Пользователь запросил помощь. 
    Доступные материалы: {materials}
    Сгенерируй персонализированный ответ. [/INST]
    """
    
    # Получаем ответ от локальной Llama
    response = await ai_client.generate_edu_response(prompt)
    
    # Отправляем пользователю
    await message.answer(response[:4000],  # Ограничение Telegram
        reply_markup=build_rating_keyboard()
    )
```

---

## Дотреивание модели

1. Создайте файл с промптами `docs/prompts/edu-assistant.txt`:
```
[INST] 
<<SYS>>
Ты — помощник для образовательной платформы. Отвечай на русском.
Используй только материалы из базы. Формат ответа:
1. Основная рекомендация
2. Ссылки на материалы в формате [ID]
<</SYS>>
Пользователь: Нужно подготовиться к экзамену по матану
[/INST]
```

2. Дообучите модель через llama.cpp:
```bash
./llama.cpp/finetune \
    --model models/llama-3-8b.Q4_K_M.gguf \
    --train-data docs/prompts/edu-assistant.txt \
    --threads 8 \
    --sample-start "[INST]"
```

---

## Оптимизация производительности

1. Используйте квантованные модели (Q4_K_M)
2. Для CPU-режима:
```python
llm = Llama(
    model_path="...",
    n_threads=8,
    n_batch=512,
    offload_kqv=True
)
```
3. Кешируйте частые запросы в Redis:
```python
async def get_cached_response(prompt: str):
    cached = await redis.get(f"response:{hash(prompt)}")
    if cached:
        return cached
    response = await generate_response(prompt)
    await redis.setex(f"response:{hash(prompt)}", 3600, response)
    return response
```

---

## Пример взаимодействия

1. Пользователь: "Помоги с интегралами"
2. Бот формирует промпт:
```
[INST] Доступные материалы: 
[123] Лекция "Интегралы", рейтинг 4.5
[456] Семинар "Практика интегрирования"

Запрос: Помоги с интегралами [/INST]
```
3. Ответ Llama:
```
Рекомендую изучить основы из лекции [123], 
затем закрепить знания на семинаре [456].
```
4. Бот показывает ответ с кнопками для оценки материалов 123 и 456.

---

## Рекомендации для хакатона

1. Используйте 7B-модели для экономии ресурсов
2. Для CPU-режима ограничьте `max_tokens` (≤512)
3. Добавьте прогресс-бар для долгих запросов:
```python
await message.answer_chat_action("typing")
```
4. Реализуйте очередь запросов через Redis
5. Используйте шаблоны ответов для стабильности:
```python
prompt += "\nОтвет должен содержать минимум 3 рекомендации..."
```

---

## Пример Docker-запуска

```bash
# С поддержкой NVIDIA GPU
docker compose up --build

# Только CPU (добавьте в docker-compose.yml)
llama-api:
  environment:
    - LLAMA_CPP_LIB=.../libllama.so  # Собранная CPU-версия
```

Интегрируем модель **DeepSeek-V3** локально в ваш проект. Пошаговая инструкция:

---

## 1. Подготовка модели
### 1.1. Скачивание модели
1. Перейдите на страницу модели:  
   [https://huggingface.co/deepseek-ai/DeepSeek-V3-0324](https://huggingface.co/deepseek-ai/DeepSeek-V3-0324)
2. Убедитесь, что у вас есть доступ (требуется заполнить форму на HF).
3. Клонируйте репозиторий:
```bash
git lfs install
git clone https://huggingface.co/deepseek-ai/DeepSeek-V3-0324
```

### 1.2. Конвертация в GGUF (для llama.cpp)
Если модель в формате PyTorch:
```bash
# Установите llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

# Конвертация
python3 convert.py --input-dir ../DeepSeek-V3-0324 --output-dir ./models/deepseek --vocab-type bpe
```

---

## 2. Настройка Docker-окружения
### 2.1. Структура проекта
```
deepseek-bot/
├── docker-compose.yml
├── bot/                      # Телеграм-бот
│   └── services/deepseek.py  # Клиент для DeepSeek
├── deepseek-api/             # Локальный ИИ-сервис
│   ├── app/
│   │   ├── main.py           # FastAPI эндпоинты
│   │   └── model_loader.py
│   ├── models/               # Модель в GGUF
│   └── Dockerfile
└── .env
```

### 2.2. Dockerfile для ИИ-сервиса
```dockerfile
FROM nvidia/cuda:12.2.0-base

WORKDIR /app
COPY . .

RUN apt-get update && \
    apt-get install -y python3.10 python3-pip && \
    pip install torch transformers fastapi uvicorn

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
```

### 2.3. docker-compose.yml
```yaml
version: '3.8'

services:
  deepseek-api:
    build: ./deepseek-api
    volumes:
      - ./deepseek-api/models:/app/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
    ports:
      - "8002:8002"
```

---

## 3. Локальный API для DeepSeek-V3
### 3.1. Загрузка модели (`model_loader.py`)
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = None
tokenizer = None

def load_model():
    global model, tokenizer
    model = AutoModelForCausalLM.from_pretrained(
        "/app/models/DeepSeek-V3-0324",
        device_map="auto",
        torch_dtype="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained("/app/models/DeepSeek-V3-0324")
```

### 3.2. FastAPI эндпоинты (`main.py`)
```python
from fastapi import FastAPI
from model_loader import load_model, model, tokenizer

app = FastAPI()

@app.on_event("startup")
async def startup():
    load_model()

@app.post("/generate")
async def generate(prompt: str, max_tokens: int = 200):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=0.7
    )
    return {"response": tokenizer.decode(outputs[0])}
```

---

## 4. Интеграция с ботом
### 4.1. Клиент для DeepSeek API
```python
# bot/services/deepseek.py
import aiohttp
from config import settings

class DeepSeekClient:
    def __init__(self):
        self.base_url = settings.DEEPSEEK_API_URL
        
    async def generate_response(self, user_query: str, context: str) -> str:
        prompt = f"""
        <|system|>
        Ты — образовательный ассистент. Отвечай на русском. 
        Контекст: {context}
        </s>
        <|user|>
        {user_query}
        </s>
        <|assistant|>
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/generate",
                json={"prompt": prompt, "max_tokens": 512}
            ) as response:
                data = await response.json()
                return data.get("response", "")
```

### 4.2. Обработчик в боте
```python
# bot/handlers/deepseek_helper.py
from aiogram import Router, F
from aiogram.types import Message
from services.deepseek import DeepSeekClient

router = Router()
deepseek = DeepSeekClient()

@router.message(F.text == "DeepSeek Помощник")
async def handle_deepseek(message: Message):
    # Получаем контекст из API веб-сервиса
    context = await get_educational_context(message.from_user.id)
    
    # Генерируем ответ
    response = await deepseek.generate_response(
        message.text, 
        context
    )
    
    await message.answer(response[:4000])
```

---

## 5. Оптимизации
1. **Квантование** (если используется GGUF):
```bash
./llama.cpp/quantize ./models/deepseek/ggml-model-f16.gguf ./models/deepseek/ggml-model-q4_k.gguf q4_k
```

2. **Кеширование ответов**:
```python
# Добавьте Redis
import redis
r = redis.Redis()

async def get_cached_response(prompt: str):
    key = f"deepseek:{hash(prompt)}"
    cached = r.get(key)
    if cached:
        return cached.decode()
    # ... генерация и сохранение в Redis
```

---

## 6. Запуск
```bash
# Собрать и запустить
docker compose build
docker compose up -d

# Проверить работу API
curl -X POST http://localhost:8002/generate -H "Content-Type: application/json" -d '{"prompt":"Что такое интеграл?"}'
```

---

## Особенности DeepSeek-V3
1. **Токенизация**: Использует специальные токены для ролей:
```python
prompt = "<|system|>\nТы помощник...</s>\n<|user|>\nВопрос...</s>\n<|assistant|>\n"
```

2. **Контекстное окно**: 32k токенов (уточните в документации модели).

3. **Аппаратные требования**:
   - Минимум 24GB VRAM для FP16
   - 16GB RAM для квантованной версии

---

## Пример промпта для обучения
```txt
<|system|>
Ты — ассистент математического курса. Отвечай строго по материалам платформы.
Доступные материалы: [123] Лекция по интегралам, [456] Семинар по производным.
</s>
<|user|>
Объясните, как решать интегралы методом подстановки.
</s>
<|assistant|>
Для решения интегралов методом подстановки (см. материал [123]):
1. Выберите часть интеграла для замены...
```



