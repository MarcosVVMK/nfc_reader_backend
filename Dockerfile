# Use the official Python 3.12 image
FROM python:3.13.7-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry

# Configure poetry: Don't create a virtual environment
ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN poetry config virtualenvs.create false

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
COPY app/README.md /app/README.md
RUN poetry lock
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]