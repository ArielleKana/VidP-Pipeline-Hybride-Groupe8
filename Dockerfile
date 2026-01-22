FROM python:3.9-slim

WORKDIR /project

# Installation de ffmpeg (obligatoire pour le traitement vidéo)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copie des besoins
COPY requirements.txt .

# --- CORRECTION ICI ---
# On installe tout ce qu'il y a dans requirements.txt avec un temps d'attente allongé
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Copie du reste du code
COPY . .

# Commande par défaut (sera écrasée par le docker-compose)
CMD ["python", "app/app.py"]