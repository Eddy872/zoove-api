from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import io
import logging

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import soundfile as sf
from scipy.signal import resample
from openai import OpenAI


logging.basicConfig(level=logging.INFO)

app = FastAPI()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

TARGET_SAMPLE_RATE = 16000
THRESHOLD = 0.5

print("✅ Lancement de l'API Zoove")

print("Chargement YAMNet...")
yamnet_model = hub.load("https://tfhub.dev/google/yamnet/1")
print("✅ YAMNet chargé")

print("Chargement AnimalClassifier...")
classifier = tf.keras.models.load_model("animal_other_classifier.keras")
print("✅ AnimalClassifier chargé")


class ChatRequest(BaseModel):
    species: str
    message: str


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l’API Zoove 🤖"}


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.post("/chat")
def chat_with_zoove(req: ChatRequest):
    prompt = f"Animal : {req.species}\nUtilisateur : {req.message}\nZoove :"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Tu es Zoove, un assistant animalier intelligent. Réponds directement, en 1 phrase courte."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=80
    )

    return {"response": response.choices[0].message.content.strip()}


def load_audio_from_bytes(file_bytes: bytes) -> np.ndarray:
    audio_io = io.BytesIO(file_bytes)
    waveform, sr = sf.read(audio_io, dtype="float32")

    if waveform.ndim == 2:
        waveform = np.mean(waveform, axis=1)

    if sr != TARGET_SAMPLE_RATE:
        new_length = int(len(waveform) * TARGET_SAMPLE_RATE / sr)
        waveform = resample(waveform, new_length)

    return waveform.astype(np.float32)


def extract_yamnet_embedding(waveform: np.ndarray) -> np.ndarray:
    scores, embeddings, spectrogram = yamnet_model(waveform)
    embedding_mean = tf.reduce_mean(embeddings, axis=0).numpy()
    embedding_mean = np.expand_dims(embedding_mean, axis=0).astype(np.float32)
    return embedding_mean


def predict_animal_or_other(waveform: np.ndarray):
    embedding = extract_yamnet_embedding(waveform)

    prob = classifier.predict(embedding, verbose=0)[0][0]
    prob = float(prob)

    label = "animal" if prob >= THRESHOLD else "other"

    return {
        "label": label,
        "animal_probability": prob,
        "other_probability": 1.0 - prob,
        "threshold": THRESHOLD
    }


@app.post("/classify-audio")
async def classify_audio(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        waveform = load_audio_from_bytes(file_bytes)

        if len(waveform) == 0:
            return JSONResponse(
                status_code=400,
                content={"error": "Audio vide"}
            )

        result = predict_animal_or_other(waveform)
        return result

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
