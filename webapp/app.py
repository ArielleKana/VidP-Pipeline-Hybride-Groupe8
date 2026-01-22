from flask import Flask, render_template, request, redirect, url_for, flash
import os
import boto3
import uuid
import urllib3 
from boto3.dynamodb.conditions import Key

# --- DÉSACTIVER LES AVERTISSEMENTS SSL ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.secret_key = "super_secret_key"

# --- CONFIGURATION DES DOSSIERS ---
BASE_DIR = '/project/data'
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'videos_originales')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Création au démarrage (au cas où)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- CONFIGURATION AWS ---
REGION = os.environ.get('AWS_REGION', 'us-east-1')
DYNAMO_TABLE = 'Videop_Groupe8_MetaData'
BUCKET_NAME = 'videop-groupe8'

# --- CONNEXIONS (AVEC verify=False) ---
dynamodb = boto3.resource('dynamodb', region_name=REGION, verify=False)
table = dynamodb.Table(DYNAMO_TABLE)
s3_client = boto3.client('s3', region_name=REGION, verify=False)

@app.route('/')
def index():
    try:
        response = table.scan()
        items = response.get('Items', [])
        # Tri : les plus récents en haut
        items = items[::-1] 
    except Exception as e:
        print(f"Erreur DynamoDB: {e}", flush=True)
        items = []
    return render_template('index.html', videos=items)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)

    if file:
        # 1. GÉNÉRATION NOM UNIQUE (UUID)
        ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{str(uuid.uuid4())}{ext}"
        
        # 2. SAUVEGARDE DANS LE DOSSIER 'videos_originales'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # 👇👇👇 CORRECTIF IMPORTANT ICI 👇👇👇
        # On s'assure que le dossier existe AVANT de sauvegarder
        # (Au cas où tu aurais tout supprimé manuellement)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        # 👆👆👆 ----------------------- 👆👆👆

        file.save(filepath)
        
        print(f"🚀 Fichier reçu et sauvegardé dans 'videos_originales' : {unique_filename}", flush=True)
        return redirect(url_for('index'))

@app.route('/delete/<video_id>', methods=['POST'])
def delete_video(video_id):
    """Supprime la vidéo de DynamoDB et de S3"""
    try:
        # 1. Supprimer de S3
        s3_key = f"videos/{video_id}"
        
        try:
            s3_client.delete_object(Bucket=BUCKET_NAME, Key=s3_key)
            print(f"🗑️ Fichiers S3 supprimés pour {video_id}", flush=True)
        except Exception as e:
            print(f"⚠️ Erreur suppression S3: {e}", flush=True)

        # 2. Supprimer de DynamoDB
        table.delete_item(Key={'video_id': video_id})
        print(f"✅ Entrée DynamoDB supprimée : {video_id}", flush=True)
        
    except Exception as e:
        print(f"❌ Erreur lors de la suppression : {e}", flush=True)
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)