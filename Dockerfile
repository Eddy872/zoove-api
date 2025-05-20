FROM python:3.11-slim

# Crée et entre dans le dossier
WORKDIR /app

# Copie le code
COPY . .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port (optionnel)
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "zoove_api:app", "--host", "0.0.0.0", "--port", "8000"]