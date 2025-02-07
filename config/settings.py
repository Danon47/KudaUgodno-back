import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "anywhere.god-it.ru",
    "anywhere-test.god-it.ru",
    "anywhere-dev.god-it.ru",
    "82.202.137.38",
]

INSTALLED_APPS = [
   # Стандартные Django-приложения
   "django.contrib.admin",
   "django.contrib.auth",
   "django.contrib.contenttypes",
   "django.contrib.sessions",
   "django.contrib.messages",
   "django.contrib.staticfiles",

   # Сторонние библиотеки
   "rest_framework",
   "rest_framework.authtoken",
   "rest_framework_simplejwt",
   "dj_rest_auth",
   "allauth",
   "allauth.account",
   "allauth.socialaccount",

   # Подключаем OAuth-авторизацию (если нужны соцсети)
   "allauth.socialaccount.providers.google",
   "allauth.socialaccount.providers.vk",
   "allauth.socialaccount.providers.yandex",

   # Дополнительные библиотеки
   "drf_spectacular",
   "phonenumber_field",
   "django_celery_beat",

   # Наши приложения
   "users",
   "tours",
   "flights",
   "hotels",
   "applications",

   # Поддержка CORS
   "corsheaders",
]

MIDDLEWARE = [
   "django.middleware.security.SecurityMiddleware",
   "django.contrib.sessions.middleware.SessionMiddleware",
   "corsheaders.middleware.CorsMiddleware",
   "django.middleware.common.CommonMiddleware",

   # 🔹 Добавляем сюда (ВАЖНО: перед AuthenticationMiddleware)
   "allauth.account.middleware.AccountMiddleware",

   "django.middleware.csrf.CsrfViewMiddleware",
   "django.contrib.auth.middleware.AuthenticationMiddleware",
   "django.contrib.messages.middleware.MessageMiddleware",
   "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]
elif not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Ограничение на размер загружаемого файла в 10 мегабайт
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "API приложения Куда Угодно",
    "DESCRIPTION": "Полная документация API приложения Куда Угодно",
    "VERSION": "0.3.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "TYPESCRIPT_GENERATOR": {
        "TYPED_PATH_PARAMETERS": True
    },
    "TAGS": [
        {"name": "Пользователи", "description": "Методы для работы с пользователями"},
        {"name": "Туры", "description": "Методы для работы с турами"},
        {"name": "Отель", "description": "Методы для работы с отелями"},
        {"name": "Удобства общие в отеле", "description": "Методы для работы с общими удобствами отелей"},
        {"name": "Удобства в номере в отеле", "description": "Методы для работы с удобствами в номерах отелей"},
        {"name": "Удобства спорт и отдых в отеле", "description": "Методы для работы с удобствами спорта и отдыха"},
        {"name": "Удобства для детей в отеле", "description": "Методы для работы с удобствами для детей"},
        {"name": "Правила в отеле", "description": "Методы для работы с правилами отелей"},
        {"name": "Фотографии в отеле", "description": "Методы для работы с фотографиями отелей"},
        {"name": "Номер", "description": "Методы для работы с номерами"},
        {"name": "Категории номера", "description": "Методы для работы с категориями номеров"},
        {"name": "Удобства в номере", "description": "Методы для работы с удобствами номеров"},
        {"name": "Фотографии номера", "description": "Методы для работы с фотографиями номеров"},
        {"name": "Рейсы", "description": "Методы для работы с рейсами"},
        {"name": "Заявки", "description": "Методы для работы с заявками"},
        {"name": "Гости", "description": "Методы для работы с гостями"},
    ],
    "SORT_OPERATIONS": True,
}

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Разрешенные домены для CORS (кросс-доменных запросов)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://anywhere-dev.god-it.ru",
    "https://anywhere-test.god-it.ru",
]

# Для продакшена добавляем HTTPS-домены и IP
if not DEBUG:
    CORS_ALLOWED_ORIGINS += [
        "https://anywhere.god-it.ru",
    ]

CSRF_TRUSTED_ORIGINS = [
    "https://anywhere.god-it.ru",
    "https://anywhere-dev.god-it.ru",
    "https://anywhere-test.god-it.ru",
]
