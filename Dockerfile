FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./alembic.ini /app/
COPY ./entrypoint.sh /app/
COPY ./static /app/static
COPY ./alembic /app/alembic
COPY ./app /app/app