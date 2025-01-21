FROM python:3.12-slim

WORKDIR /app

# Копируем только файл с зависимостями
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry и зависимости
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root && \
    pip cache purge

# Копируем остальной код проекта
COPY . .

# Создаём пользователя и заходим под ним
RUN useradd -m backenduser && \
    chown -R backenduser:backenduser /app && \
    mkdir -p /app/celery_beat && \
    chown -R backenduser:backenduser /app/celery_beat
USER backenduser
