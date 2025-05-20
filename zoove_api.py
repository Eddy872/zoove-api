from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI
import logging

# 🔐 Initialise le client OpenAI avec clé API depuis les variables d'env
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 🧠 Logs
logging.basicConfig(level=logging.INFO)
print("✅ Lancement de l'API Zoove avec GPT-3.5...")

app = FastAPI()

class Request(BaseModel):
    species: str
    message: str

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l’API Zoove 🤖"}

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/chat")
def chat_with_zoove(req: Request):
    print("📥 Requête reçue")

    # 📝 Construction du prompt en langage naturel
    prompt = f"""Tu es Zoove, un assistant expert en comportement animal.
Réponds toujours en français, de manière bienveillante et claire.

Espèce : {req.species}
Utilisateur : {req.message}
Zoove :"""

    print(f"📝 Prompt envoyé à OpenAI :\n{prompt}")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es Zoove, un assistant animalier intelligent."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )

    print("✅ Réponse générée")
    return {"response": response.choices[0].message.content.strip()}
