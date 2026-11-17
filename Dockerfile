FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ ./src/
COPY services.yaml .

RUN pip install --no-cache-dir -e .

CMD ["python", "-m", "tor_monitor.monitor"]
