FROM python:3.12-slim

WORKDIR /app

# Копируем только файл с зависимостями
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry и зависимости
RUN pip install poetry=1.8.5 && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev-- no-root

# Копируем остальной код проекта
COPY . .