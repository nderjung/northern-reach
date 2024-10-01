# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    PATH="/root/.local/bin:$PATH" \
    POETRY_VIRTUALENVS_CREATE=false

# Install dependencies and poetry in one layer
RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock to install dependencies
COPY pyproject.toml poetry.lock* ./

# Install Python dependencies
RUN poetry install --no-interaction --no-ansi

# Copy application code
COPY ./northern_reach /app
