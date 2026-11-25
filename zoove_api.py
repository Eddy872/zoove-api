from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI, OpenAIError
import os
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zoove-api")

# Configuration OpenAI
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-6-luna")

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    timeout=30.0,
    max_retries=1
)

logger.info("Lancement de l'API Zoove avec %s", OPENAI_MODEL)

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

    logger.info("📥 Requête reçue")

    prompt = (
        f"Animal : {req.species}\n"
        f"Utilisateur : {req.message}\n"
        "Zoove :"
    )

    try:

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es Zoove, un assistant animalier intelligent."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            reasoning_effort="none",
            max_completion_tokens=150
        )

        content = response.choices[0].message.content

        if not content or not content.strip():
            logger.error("Réponse OpenAI vide")

            raise HTTPException(
                status_code=502,
                detail="Réponse OpenAI vide"
            )

        if response.usage:
            logger.info(
                "Tokens entrants : %s | Tokens sortants : %s",
                response.usage.prompt_tokens,
                response.usage.completion_tokens
            )

        logger.info("✅ Réponse générée")

        return {"response": content.strip()}

    except OpenAIError as error:

        logger.error(
            "❌ Erreur OpenAI : %s | HTTP : %s | Code : %s",
            type(error).__name__,
            getattr(error, "status_code", None),
            getattr(error, "code", None)
        )

        raise HTTPException(
            status_code=502,
            detail="Service de génération temporairement indisponible"
        ) from error
