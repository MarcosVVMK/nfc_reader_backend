FROM python:3.13.7-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
COPY app/README.md /app/README.md
RUN poetry lock
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]