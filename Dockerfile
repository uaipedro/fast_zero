FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

ENV POETRY_VERSION 1.7.1

RUN pip install "poetry==$POETRY_VERSION"

RUN poetry install --no-root --no-directory

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi
RUN poetry run alembic upgrade head

EXPOSE 8001
CMD [ "poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8001", "fast_zero.app:app" ]