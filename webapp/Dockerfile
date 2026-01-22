# On utilise une version légère de Python pour le site web
FROM python:3.9-slim

# On se place dans le dossier /app du conteneur
WORKDIR /app

# On copie les besoins du site (Flask, boto3)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie le code du site (app.py et les templates)
COPY . .

# On ouvre le port 5000 pour accéder au site
EXPOSE 5000

# La commande pour lancer le site
CMD ["python", "app.py"]