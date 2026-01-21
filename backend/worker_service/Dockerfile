FROM python:3.14-slim

WORKDIR /worker

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "worker.consumer"]