FROM python:3.12
WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

WORKDIR /app/src
