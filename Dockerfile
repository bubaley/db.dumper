FROM python:3.12-alpine3.19

RUN pip install poetry==1.8.3
ENV POETRY_VIRTUALENVS_CREATE 0

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root --no-interaction --no-ansi --no-cache
COPY . ./
