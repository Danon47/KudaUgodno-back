import os
from pathlib import Path
from dotenv import load_dotenv

from all_fixture.fixture_views import (
    user_settings,
    tour_settings,
    hotel_settings,
    hotel_photo_settings,
    room_settings,
    room_photo_settings,
    flight_settings,
    application_settings,
    application_guest_settings,
    # room_category_settings,
    # room_amenity_settings,
    # hotel_amenity_children_settings,
    # hotel_rules_settings,
    # hotel_amenity_common_settings,
    # hotel_amenity_room_settings,
    # hotel_amenity_sport_settings,
)


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
    "ku.mer1d1an.ru",
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

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "static/media"

# Ограничение на размер загружаемого файла в 10 мегабайт
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "API приложения Куда Угодно",
    "DESCRIPTION": "Полная документация API приложения Куда Угодно",
    "VERSION": "0.5.1",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "TYPESCRIPT_GENERATOR": {"TYPED_PATH_PARAMETERS": True},
    "TAGS": [
        user_settings,
        tour_settings,
        hotel_settings,
        # hotel_amenity_common_settings,
        # hotel_amenity_room_settings,
        # hotel_amenity_sport_settings,
        # hotel_amenity_children_settings,
        # hotel_rules_settings,
        hotel_photo_settings,
        room_settings,
        # room_category_settings,
        # room_amenity_settings,
        room_photo_settings,
        flight_settings,
        application_settings,
        application_guest_settings,
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
    "http://127.0.0.1:8000",
    "https://ku.mer1d1an.ru",
    "https://anywhere-dev.god-it.ru",
    "https://anywhere-test.god-it.ru",
]

# Для продакшена добавляем HTTPS-домены и IP
if not DEBUG:
    CORS_ALLOWED_ORIGINS += [
        "https://anywhere.god-it.ru",
    ]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "https://ku.mer1d1an.ru",
    "https://anywhere.god-it.ru",
    "https://anywhere-dev.god-it.ru",
    "https://anywhere-test.god-it.ru",
]

DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000