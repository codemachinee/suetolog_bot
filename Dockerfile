# Используем образ с uv для сборщика
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
# устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*
# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости в рабочую директорию
COPY pyproject.toml uv.lock ./

# синхронизируем зависимости, удаляем лишнее
RUN uv sync && \
    rm -rf /root/.cache && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
# Копируем остальные файлы проекта в рабочую директорию
COPY . .

# Используем образ с uv для переноса только файлов и зависимостей проекта без лишней нагрузки
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Копия со слоя билдера только папки с проектом
COPY --from=builder /app /app

# Запускаем бота
CMD ["uv","run","python", "main.py"]