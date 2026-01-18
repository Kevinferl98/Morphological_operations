FROM python:3.14.2

WORKDIR /app

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

ENV FLASK_ENV=dev
ENV FLASK_APP=app
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV REDIS_URL=redis://redis:6379/0

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "run:app", "--workers", "4", "--threads", "2", "--timeout", "120"]