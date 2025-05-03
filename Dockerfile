# Base Python image
FROM python:3.10

# Dossier de travail dans le conteneur
WORKDIR /app

# Copier tout le contenu de notebooks/ (code + modèle + requirements)
COPY ./notebooks /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8000 (utilisé par uvicorn)
EXPOSE 8000

# Lancer FastAPI avec uvicorn
CMD ["uvicorn", "zoove_api:app", "--host", "0.0.0.0", "--port", "8000"]