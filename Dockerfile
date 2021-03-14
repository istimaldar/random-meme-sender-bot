FROM python:3.9.2-alpine3.12
ENV POETRY_HOME=/opt/poetry/
ENV POETRY_VERSION=1.1.4
ENV PATH=/opt/poetry/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin


RUN apk add curl && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev -n

COPY . .
ENTRYPOINT ["poetry", "run", "python", "random_memes_sender.py"]
