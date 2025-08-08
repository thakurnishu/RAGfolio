FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.7.15 /uv /uvx /bin/

WORKDIR /app

ADD uv.lock /app/uv.lock
ADD pyproject.toml /app/pyproject.toml
RUN uv sync --locked

ADD . /app

EXPOSE 8501

CMD [ "uv", "run", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
