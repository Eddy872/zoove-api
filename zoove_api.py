from fastapi import FastAPI
from pydantic import BaseModel
from transformers import T5ForConditionalGeneration, T5Tokenizer
print("🧠 Chargement du modèle depuis Hugging Face...")
import logging
logging.basicConfig(level=logging.INFO)
print("✅ Lancement de l'API Zoove...")


app = FastAPI()
tokenizer = T5Tokenizer.from_pretrained("Eddy872/zoove-t5")
model = T5ForConditionalGeneration.from_pretrained("Eddy872/zoove-t5")
model.eval()
print("✅ Modèle chargé avec succès")

class Request(BaseModel):
    species: str
    message: str

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l’API Zoove 🤖"}

@app.post("/chat")
def chat_with_zoove(req: Request):
    prompt = f"{req.species}. {req.message}"
    inputs = tokenizer(prompt, return_tensors="pt", max_length=64, truncation=True, padding="max_length")
    output = model.generate(
        inputs["input_ids"],
        max_length=64,
        num_beams=4,
        early_stopping=True,
        eos_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"response": response}
