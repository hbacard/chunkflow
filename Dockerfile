FROM python:3.12-slim

WORKDIR /app

RUN pip install -U pdm

COPY pyproject.toml pdm.lock README.md ./

COPY src ./src

COPY mcp ./mcp

RUN pdm sync 

USER 1000

EXPOSE 8001

CMD ["pdm", "run", "python", "mcp/server.py"]