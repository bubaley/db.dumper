FROM python:3.12-alpine3.19

RUN pip install poetry==1.8.3
RUN apk add --no-cache postgresql-client
ENV POETRY_VIRTUALENVS_CREATE 0

WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY config.yaml config.yaml ./

RUN poetry install --without dev --no-root --no-interaction --no-ansi --no-cache
COPY . ./
