FROM python:3.11-slim

WORKDIR /ui

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./
COPY app.py ./

RUN pip install --no-cache-dir poetry==2.0.1 \
    && poetry install --no-interaction

COPY src ./src

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
