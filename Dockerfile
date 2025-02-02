FROM python:3.12.8

WORKDIR /app

# Копируем только файл с зависимостями
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry и зависимости
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root && \
    pip cache purge

# Создаём пользователя и заходим под ним
RUN groupadd -g 1003 backendusergroup && \
    useradd -u 1001 -g 1003 -m -o backenduser && \
    chown -R backenduser:backendusergroup /app && \

USER backenduser

# Копируем остальной код проекта
COPY . .


