#!/usr/bin/env bash
set -e

# === Функция: ожидание доступности PostgreSQL ===
wait_for_postgres() {
    echo "Ожидание готовности базы данных PostgreSQL..."
    python << END
import time
import asyncpg
import asyncio
import os

dsn = os.environ.get("POSTGRES_DSN")
if not dsn:
    raise RuntimeError("POSTGRES_DSN не задан")

async def wait_for_db():
    while True:
        try:
            conn = await asyncpg.connect(dsn)
            await conn.close()
            print("PostgreSQL доступна.")
            break
        except Exception as e:
            print(f"PostgreSQL недоступна: {e}. Жду...")
            time.sleep(2)

asyncio.run(wait_for_db())
END
}

# === Функция: создание схемы 'ku' ===
# create_schema_ku() {
#     echo "Добавление схемы 'ku'..."
#     python << END
# import asyncpg
# import asyncio
# import os

# dsn = os.environ.get("POSTGRES_DSN")
# if not dsn:
#     raise RuntimeError("POSTGRES_DSN не задан")

# async def create_schema():
#     conn = await asyncpg.connect(dsn)
#     await conn.execute('CREATE SCHEMA IF NOT EXISTS ku;')
#     await conn.close()
#     print("Схема 'ku' успешно добавлена.")

# asyncio.run(create_schema())
# END
# }

# === Функция: проверка доступа к схеме 'ku' ===
# check_schema_access() {
#     echo "Проверка доступа к схеме 'ku'..."
#     python << END
# import asyncpg
# import asyncio
# import os

# dsn = os.environ.get("POSTGRES_DSN")
# if not dsn:
#     raise RuntimeError("POSTGRES_DSN не задан")

# async def test_schema():
#     conn = await asyncpg.connect(dsn)
#     try:
#         # Попробуем выполнить запрос к INFORMATION_SCHEMA
#         result = await conn.fetchval("SELECT COUNT(*) FROM ku.django_migrations LIMIT 1")
#         print("Схема 'ku' доступна.")
#     except Exception as e:
#         print(f"Ошибка доступа к схеме 'ku': {e}")
#         raise
#     finally:
#         await conn.close()

# asyncio.run(test_schema())
# END
# }

# === Определяем тип сервиса по переменной окружения ===
SERVICE_TYPE=${SERVICE_TYPE:-web}
case "$SERVICE_TYPE" in
  app)
    wait_for_postgres
    # create_schema_ku
    ;;
  celery_worker|celery_beat|flower)
    wait_for_postgres
    # check_schema_access
    ;;
  *)
    echo "Неизвестный тип сервиса: $SERVICE_TYPE" >&2
    exit 1
    ;;
esac

# === Выполняем действия в зависимости от типа сервиса ===
case "$SERVICE_TYPE" in
  app)
    echo "Загрузка collectstatic"
    python3 manage.py collectstatic --noinput

    echo "Применение миграций"
    python3 manage.py makemigrations --noinput
    python3 manage.py migrate --noinput

    echo "Создание данных"
    python3 manage.py c_hotel

    echo "Старт Gunicorn"
    exec gunicorn config.wsgi:application \
        --bind "${GUNICORN_HOST}:${GUNICORN_PORT}" \
        --workers 3 \
        --timeout 120 \
        --preload
    ;;
  celery_worker)
    echo "Запуск Celery Worker"
    exec celery -A config worker --loglevel=info --concurrency=1 --max-tasks-per-child=1
    ;;
  celery_beat)
    echo "Запуск Celery Beat"
    exec celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    ;;
  flower)
    echo "Запуск Flower"
    exec celery -A config flower --port=${CELERY_FLOWER_PORT} --broker=${CELERY_BROKER_URL}
    ;;
esac
