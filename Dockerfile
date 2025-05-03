FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn transformers torch sentencepiece

EXPOSE 8000

CMD ["uvicorn", "zoove_api:app", "--host", "0.0.0.0", "--port", "8000"]
