FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.7.15 /uv /uvx /bin/

ADD . /app

WORKDIR /app

RUN uv sync --locked 

EXPOSE 8000

CMD [ "uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000" ]
