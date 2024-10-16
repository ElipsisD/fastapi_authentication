FROM python:3.12 AS builder

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.3 POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"
RUN poetry self add poetry-plugin-export

WORKDIR /tmp

COPY pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12
LABEL authors="Dmitry"

# Python environments.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt

COPY --from=builder /tmp/requirements.txt /opt/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /opt/requirements.txt

COPY .. /opt

CMD ["uvicorn", "statistic_app.main:app", "--port", "8003", "--host", "0.0.0.0", "--reload"]
