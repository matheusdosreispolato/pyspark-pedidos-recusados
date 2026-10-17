FROM python:3.11-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jre-headless git procps \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
