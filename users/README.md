# 📱 Phone Auth System - Реферальная система с авторизацией по телефону

Современная система авторизации по номеру телефона с реферальной программой, построенная на Django и Django REST Framework.

## 🌟 Особенности

- ✅ **Двойной интерфейс** - REST API + Веб-интерфейс в одном проекте
- ✅ **Авторизация по SMS** - Двухэтапная авторизация без паролей
- ✅ **Автоматическая регистрация** - Создание пользователя при первом входе
- ✅ **Реферальная система** - Уникальные инвайт-коды и отслеживание рефералов
- ✅ **REST API** - Полноценное API для мобильных и веб-приложений
- ✅ **Веб-интерфейс** - Готовый интерфейс на Django Templates с современным дизайном
- ✅ **Безопасность** - Token-based аутентификация
- ✅ **Готовые тесты** - Postman коллекция и Python тесты
- ✅ **ReDoc документация** - Автоматическая генерация интерактивной документации
- ✅ **Документация** - Подробная API документация и примеры

## 🎯 Два способа использования

### 📱 REST API - для мобильных приложений
```bash
# Отправка SMS-кода
POST /api/users/send-code/
# Верификация кода  
POST /api/users/verify-code/
# Получение профиля
GET /api/users/profile/
# Активация инвайта
POST /api/users/activate-invite/
```

### 🌐 Веб-интерфейс - для браузера
```bash
# Главная страница
GET /users/
# Подтверждение кода
GET /users/verify/
# Профиль пользователя
GET /users/profile/
```

## 🚀 Быстрый старт

### Локальная разработка

```bash
# Клонирование проекта
git clone <repository-url>
cd phone_auth_system

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt

# Настройка базы данных
python manage.py makemigrations
python manage.py migrate

# Создание суперпользователя (опционально)
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver
```

### Деплой на PythonAnywhere

```bash
# В Bash консоли PythonAnywhere
cd ~
git clone <repository-url> phone_auth_system
cd phone_auth_system

# Создание виртуального окружения
mkvirtualenv --python=/usr/bin/python3.10 phoneauth
workon phoneauth

# Установка зависимостей
pip install -r requirements.txt

# Настройка базы данных
python manage.py migrate
python manage.py collectstatic --noinput
```

## 📋 Технические требования

- **Python**: 3.8+
- **Django**: 4.2.7
- **Django REST Framework**: 3.14.0
- **База данных**: SQLite (по умолчанию) / PostgreSQL (продакшен)

## 🏗️ Архитектура проекта

```
PHONE_AUTH_SYSTEM/
├── auth_project/                    # Основные настройки Django
│   ├── __pycache__/                # Кэш Python файлов
│   ├── __init__.py                 # Пакет Python
│   ├── asgi.py                     # ASGI конфигурация
│   ├── settings.py                 # Настройки проекта
│   ├── urls.py                     # Главные URL маршруты
│   └── wsgi.py                     # WSGI конфигурация
├── users/                          # Основное приложение
│   ├── migrations/                 # Миграции базы данных
│   ├── static/users/              # Статические файлы приложения
│   │   ├── css/                   # CSS стили
│   │   │   └── style.css          # Основные стили
│   │   └── js/                    # JavaScript файлы
│   │       └── app.js             # Основная логика JS
│   ├── templates/users/           # HTML шаблоны
│   │   ├── base.html              # Базовый шаблон
│   │   ├── index.html             # Главная страница
│   │   ├── profile.html           # Страница профиля
│   │   └── verify.html            # Страница подтверждения
│   ├── __init__.py                # Пакет Python
│   ├── admin.py                   # Настройки админки
│   ├── apps.py                    # Конфигурация приложения
│   ├── models.py                  # Модели User и PhoneVerification
│   ├── test_api.py                # Тесты API
│   ├── tests.py                   # Основные тесты
│   ├── urls.py                    # URL маршруты приложения
│   ├── views.py                   # API views (REST Framework)
│   └── web_views.py               # Web interface views (Django Templates)
├── venv/                          # Виртуальное окружение Python
├── db.sqlite3                     # База данных SQLite
├── debug.log                      # Логи приложения
├── manage.py                      # Django management команды
├── phone_auth_system.tar.gz       # Архив проекта
├── Phone Auth System.postman_collection.json  # Postman коллекция
├── README.md                      # Документация проекта
└── requirements.txt               # Зависимости Python
```

### 🎯 Ключевые компоненты

#### **auth_project/** - Основная конфигурация
- `settings.py` - Настройки Django, база данных, статические файлы
- `urls.py` - Главный роутинг, подключение приложений
- `wsgi.py` - Конфигурация для веб-сервера

#### **users/** - Основное приложение
- `models.py` - Модели `User` и `PhoneVerification`
- `views.py` - REST API endpoints для мобильных приложений
- `web_views.py` - Веб-интерфейс для браузера
- `urls.py` - Маршрутизация API и веб-страниц

#### **Статические файлы**
- `static/users/css/style.css` - Современные стили с градиентами
- `static/users/js/app.js` - Интерактивность и валидация форм

#### **Шаблоны**
- `base.html` - Базовый шаблон с общими стилями
- `index.html` - Форма ввода номера телефона
- `verify.html` - Форма ввода SMS-кода
- `profile.html` - Профиль пользователя и рефералы

#### **База данных**
- `db.sqlite3` - SQLite база с таблицами пользователей и верификаций
- `migrations/` - История изменений схемы БД

## 🔗 API Endpoints

### Base URLs
- **Локально**: `http://127.0.0.1:8000`
- **Продакшен**: `https://yourdomain.pythonanywhere.com`

### 📱 API маршруты

| Метод | Endpoint | Описание | Аутентификация |
|-------|----------|----------|----------------|
| `POST` | `/api/users/send-code/` | Отправка SMS-кода | Нет |
| `POST` | `/api/users/verify-code/` | Верификация кода | Нет |
| `GET` | `/api/users/profile/` | Получение профиля | Token |
| `POST` | `/api/users/activate-invite/` | Активация инвайт-кода | Token |

### 🌐 Веб-интерфейс

| URL | Страница | Описание | Файл |
|-----|----------|----------|------|
| `/` | Главная | Ввод номера телефона | `templates/users/index.html` |
| `/users/verify/` | Верификация | Ввод SMS-кода | `templates/users/verify.html` |
| `/users/profile/` | Профиль | Профиль и рефералы | `templates/users/profile.html` |

### 📚 API документация

| URL | Интерфейс | Описание |
|-----|-----------|----------|
| `/api/docs/` | **ReDoc** | Интерактивная документация API |
| `/api/swagger/` | **Swagger UI** | Альтернативный интерфейс документации |
| `/api/schema/` | **OpenAPI Schema** | JSON схема API |
| `/api/` | **API Info** | Общая информация о API |

| Файл | Назначение |
|------|------------|
| `Phone Auth System.postman_collection.json` | Готовая Postman коллекция для тестирования API |
| `test_api.py` | Python скрипты для тестирования API |
| `debug.log` | Логи приложения Django |
### 📁 Дополнительные файлы

| Файл | Назначение |
|------|------------|
| `Phone Auth System.postman_collection.json` | Готовая Postman коллекция для тестирования API |
| `test_api.py` | Python скрипты для тестирования API |
| `debug.log` | Логи приложения Django |
| `phone_auth_system.tar.gz` | Архив проекта для резервного копирования |

## 📖 Интерактивная документация

### 🎯 ReDoc - Основная документация
**URL**: `https://yourdomain.com/api/docs/`

Красивая интерактивная документация с:
- 📋 Подробным описанием всех endpoints
- 🎨 Примерами запросов и ответов
- 🔐 Информацией об аутентификации
- 📊 Схемами данных
- 🏷️ Тегированием по категориям

### ⚡ Swagger UI - Тестирование
**URL**: `https://yourdomain.com/api/swagger/`

Интерфейс для тестирования API:
- 🧪 Выполнение запросов прямо в браузере
- 🔑 Поддержка авторизации
- 📝 Валидация запросов
- 📈 Отображение ответов в реальном времени

### 🔧 OpenAPI Schema
**URL**: `https://yourdomain.com/api/schema/`

JSON схема для:
- 🛠️ Генерации клиентских SDK
- 📚 Интеграции с другими системами
- 🔄 Автоматического тестирования
- 📋 Валидации API контрактов

## 📖 Подробная документация API

### 1. Отправка SMS-кода

**Endpoint**: `POST /api/users/send-code/`

Отправляет 4-значный код верификации на указанный номер телефона.

#### Запрос
```json
{
    "phone_number": "+375294567892"
}
```

#### Успешный ответ (200)
```json
{
    "message": "Код отправлен на номер",
    "phone_number": "+375294567892",
    "verification_code": "1234"
}
```

#### Ошибки
- **400 Bad Request**: Номер телефона не указан

```json
{
    "error": "Номер телефона обязателен"
}
```

#### Пример cURL
```bash
curl -X POST http://127.0.0.1:8000/api/users/send-code/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+375294567892"}'
```

### 2. Верификация кода

**Endpoint**: `POST /api/users/verify-code/`

Проверяет SMS-код и выполняет авторизацию/регистрацию пользователя.

#### Запрос
```json
{
    "phone_number": "+375294567892",
    "verification_code": "1234"
}
```

#### Успешный ответ (200)
```json
{
    "message": "Успешная авторизация",
    "token": "abc123def456789...",
    "user_id": 1,
    "phone_number": "+375294567892",
    "invite_code": "ABC123",
    "is_new_user": true
}
```

#### Ошибки
- **400 Bad Request**: Неверный код или отсутствующие данные

```json
{
    "error": "Неверный код"
}
```

#### Пример cURL
```bash
curl -X POST http://127.0.0.1:8000/api/users/verify-code/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+375294567892", "verification_code": "1234"}'
```

### 3. Получение профиля

**Endpoint**: `GET /api/users/profile/`

Возвращает информацию о пользователе и его рефералах.

#### Заголовки
```
Authorization: Token YOUR_TOKEN_HERE
```

#### Успешный ответ (200)
```json
{
    "user_id": 1,
    "phone_number": "+375294567892",
    "invite_code": "ABC123",
    "activated_invite_code": "XYZ789",
    "referrals": [
        {
            "phone_number": "+375291234567",
            "joined_date": "2025-07-26T10:30:00Z"
        }
    ],
    "referrals_count": 1
}
```

#### Ошибки
- **401 Unauthorized**: Токен не предоставлен или недействителен

```json
{
    "detail": "Authentication credentials were not provided."
}
```

#### Пример cURL
```bash
curl -X GET http://127.0.0.1:8000/api/users/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 4. Активация инвайт-кода

**Endpoint**: `POST /api/users/activate-invite/`

Активирует инвайт-код другого пользователя.

#### Заголовки
```
Authorization: Token YOUR_TOKEN_HERE
```

#### Запрос
```json
{
    "invite_code": "ABC123"
}
```

#### Успешный ответ (200)
```json
{
    "message": "Инвайт-код успешно активирован",
    "activated_invite_code": "ABC123",
    "inviter_phone": "+375294567892"
}
```

#### Ошибки
- **400 Bad Request**: Различные ошибки валидации

```json
{
    "error": "Инвайт-код не существует"
}
```

```json
{
    "error": "Вы уже активировали инвайт-код: XYZ789"
}
```

```json
{
    "error": "Нельзя активировать собственный инвайт-код"
}
```

#### Пример cURL
```bash
curl -X POST http://127.0.0.1:8000/api/users/activate-invite/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"invite_code": "ABC123"}'
```

## 📊 Модели данных

### User Model
```python
class User(AbstractUser):
    phone_number = CharField(max_length=15, unique=True)          # Номер телефона
    invite_code = CharField(max_length=6, unique=True)            # Уникальный инвайт-код
    activated_invite_code = CharField(max_length=6, null=True)    # Активированный код
    created_at = DateTimeField(auto_now_add=True)                 # Дата регистрации
```

### PhoneVerification Model
```python
class PhoneVerification(models.Model):
    phone_number = CharField(max_length=15)         # Номер телефона
    verification_code = CharField(max_length=4)     # SMS-код
    created_at = DateTimeField(auto_now_add=True)   # Время создания
    is_verified = BooleanField(default=False)       # Статус верификации
```

## 🔒 Аутентификация

Система использует **Token Authentication** из Django REST Framework.

### Получение токена
1. Отправьте SMS-код через `/api/users/send-code/`
2. Подтвердите код через `/api/users/verify-code/`
3. Получите токен в ответе

### Использование токена
Добавьте заголовок в все защищенные запросы:
```
Authorization: Token YOUR_TOKEN_HERE
```

### Управление токенами
```python
# Получение токена пользователя
from rest_framework.authtoken.models import Token
token = Token.objects.get(user=user)

# Создание нового токена
token = Token.objects.create(user=user)

# Удаление токена (logout)
token.delete()
```

## 🧪 Тестирование

### Postman коллекция

В проекте включена готовая Postman коллекция с примерами всех запросов:

1. Импортируйте `Phone Auth System.postman_collection.json`
2. Установите переменную `base_url` на ваш сервер
3. Выполните запросы в последовательности

### Автоматические тесты

```bash
# Запуск тестов
python manage.py test

# Запуск с покрытием
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Тестовый сценарий

```python
import requests

BASE_URL = 'http://127.0.0.1:8000'

# 1. Отправка кода
response = requests.post(f'{BASE_URL}/api/users/send-code/', 
                        json={'phone_number': '+375294567892'})
code = response.json()['verification_code']

# 2. Верификация
response = requests.post(f'{BASE_URL}/api/users/verify-code/', 
                        json={'phone_number': '+375294567892', 
                              'verification_code': code})
token = response.json()['token']

# 3. Профиль
headers = {'Authorization': f'Token {token}'}
response = requests.get(f'{BASE_URL}/api/users/profile/', headers=headers)
profile = response.json()
```

## 🚀 Развертывание

### PythonAnywhere

1. **Загрузка кода**:
```bash
git clone <repository-url> phone_auth_system
cd phone_auth_system
```

2. **Настройка окружения**:
```bash
mkvirtualenv --python=/usr/bin/python3.10 phoneauth
workon phoneauth
pip install -r requirements.txt
```

3. **Настройка базы данных**:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

4. **Настройка Web App**:
   - Source code: `/home/username/phone_auth_system`
   - WSGI file: Обновить пути к проекту
   - Static files: `/home/username/phone_auth_system/static`

### Docker (опционально)

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🔧 Настройки

### Переменные окружения

```bash
# .env файл
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,localhost
DATABASE_URL=postgres://user:pass@host:port/db
```

### Настройки продакшена

```python
# settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 3600
```

## 📈 Мониторинг и логирование

### Логи Django

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'app.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Метрики API

- Количество регистраций
- Успешность верификации SMS
- Активность рефералов
- Время ответа API

## 🤝 Содействие проекту

1. Форк репозитория
2. Создание feature ветки
3. Коммит изменений
4. Push в ветку
5. Создание Pull Request
