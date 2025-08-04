FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.7.15 /uv /uvx /bin/

WORKDIR /app

ADD . /app
ADD resume.pdf /app/.

RUN uv sync --locked 

EXPOSE 8501

CMD [ "uv", "run", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
