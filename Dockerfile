FROM python:3.12

# Чтобы логи сразу шли в stdout/stderr без буферизации
ENV PYTHONUNBUFFERED=1

# Устанавливаем Poetry
RUN pip install --no-cache-dir --upgrade pip && \
    pip install poetry

WORKDIR /app

# Копируем файлы конфигурации Poetry
COPY pyproject.toml poetry.lock ./

# Ставим зависимости внутрь окружения Poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

# Копируем весь остальной код
COPY . .

#EXPOSE 8000

## Запускаем Django через Poetry
#CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]