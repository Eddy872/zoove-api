FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app/zoove_chatbot && \
    mv /app/config.json /app/zoove_chatbot/ && \
    mv /app/tokenizer_config.json /app/zoove_chatbot/ && \
    mv /app/special_tokens_map.json /app/zoove_chatbot/ && \
    mv /app/spiece.model /app/zoove_chatbot/ && \
    mv /app/model.safetensors /app/zoove_chatbot/

EXPOSE 8000

CMD ["uvicorn", "zoove_api:app", "--host", "0.0.0.0", "--port", "8000"]