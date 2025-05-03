#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fastapi import FastAPI
from pydantic import BaseModel
import sentencepiece
from transformers import T5ForConditionalGeneration, T5Tokenizer


# In[6]:


app = FastAPI()

# Charger le modèle fine-tuné
tokenizer = T5Tokenizer.from_pretrained("zoove_chatbot", local_files_only=True)
model = T5ForConditionalGeneration.from_pretrained("zoove_chatbot", local_files_only=True)
model.eval()


# In[8]:


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


# In[ ]:




