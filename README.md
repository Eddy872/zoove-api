# 🐾 Zoove API - Chatbot Animalier avec FastAPI & T5

Cette API REST permet de discuter avec un modèle T5 fine-tuné, adapté aux besoins des animaux (espèce + message). Elle est conçue pour être utilisée dans une application iOS et déployée facilement via Docker et Render.

---

## 🚀 Fonctionnalités

- 🔁 Endpoint `POST /chat` : envoie un message + une espèce et reçoit une réponse générée par le modèle T5
- 🧠 Modèle fine-tuné intégré (`zoove_chatbot/`)
- 🐳 Dockerisé pour un déploiement simple
- 🔐 JSON structuré avec FastAPI + Pydantic

---
