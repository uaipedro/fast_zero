FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

<<<<<<< HEAD
RUN pip install poetry
=======
RUN pip install poetry && poetry install --no-root --no-directory
>>>>>>> bab4fa4 (fix dockerfile)

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8001
CMD [ "poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8001", "fast_zero.app:app" ]