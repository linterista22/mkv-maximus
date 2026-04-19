FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    mkvtoolnix \
    tesseract-ocr \
    tesseract-ocr-ita \
    tesseract-ocr-eng \
    mediainfo \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

RUN mkdir -p /app/data

EXPOSE 7788

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7788", "--log-level", "info"]
