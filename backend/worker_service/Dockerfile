FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OPENCV_VIDEOIO_PRIORITY_BACKEND=0

WORKDIR /worker

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system workergroup && adduser --system --group workeruser

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R workeruser:workergroup /worker

USER workeruser

CMD ["python", "-m", "worker.consumer"]