FROM python:3.12-slim


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false\
    PATH="/root/.local/bin:$PATH"


WORKDIR /app


RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean


RUN curl -sSL https://install.python-poetry.org | python3 -


COPY pyproject.toml poetry.lock /app/


RUN poetry install --no-root --no-dev


COPY . /app/


CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]