import boto3
import os
import time
import urllib3
from boto3.s3.transfer import TransferConfig

# --- DÉSACTIVATION ALERTE SÉCURITÉ (POUR DEV LOCAL) ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION MODE ÉCO (POUR ÉVITER LE CRASH RAM / CODE 137) ---
ECO_CONFIG = TransferConfig(max_concurrency=1, use_threads=False)

# --- CONFIGURATION ---
BUCKET_NAME = 'videop-groupe8'
TABLE_NAME = 'Videop_Groupe8_MetaData'
BASE_DIR = '/project/data'
FINAL_DIR = os.path.join(BASE_DIR, "videos_finales")
LANG_DIR = os.path.join(BASE_DIR, "languages_detected")
SUB_DIR = os.path.join(BASE_DIR, "sous_titres")
ANIM_DIR = os.path.join(BASE_DIR, "animaux_detectes")

REGION = os.environ.get('AWS_REGION', 'us-east-1')

# --- CONNEXION AWS ---
try:
    # verify=False permet de contourner le blocage SSL de ton antivirus/réseau
    s3 = boto3.client('s3', region_name=REGION, verify=False)
    dynamodb = boto3.resource('dynamodb', region_name=REGION, verify=False)
    table = dynamodb.Table(TABLE_NAME)
except Exception as e:
    print(f"⚠️ Erreur init AWS (Vérifiez vos clés): {e}")

def read_file_content(filepath):
    """Lit le contenu d'un fichier texte s'il existe"""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except:
            return None
    return "Non disponible"

def upload_and_index(video_filename):
    """Version robuste qui trouve les fichiers textes quoi qu'il arrive"""
    
    video_path = os.path.join(FINAL_DIR, video_filename)
    
    # On extrait l'ID unique (le début du nom avant le premier _)
    # Exemple: c2f1cce8-c7c0-40d7-b5d0-495aa49c076b
    video_uuid = video_filename.split('_')[0]

    print(f"🚀 Synchronisation DynamoDB pour l'ID : {video_uuid}", flush=True)

    try:
        # 1. UPLOAD S3
        s3_key = f"videos/{video_filename}" 
        with open(video_path, "rb") as f:
            s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=f)
        s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

        # 2. RECHERCHE INTELLIGENTE DES FICHIERS TEXTES
        # On cherche n'importe quel fichier qui COMMENCE par l'UUID dans les dossiers
        def find_content(directory, suffix):
            if os.path.exists(directory):
                for f in os.listdir(directory):
                    if f.startswith(video_uuid) and suffix in f:
                        return read_file_content(os.path.join(directory, f))
            return "Non disponible"

        langue = find_content(LANG_DIR, "langue")
        # On cherche 'subtitles' ou 'transcription'
        texte = find_content(SUB_DIR, "subtitles")
        # On cherche 'animaux' ou 'animals'
        animaux = find_content(ANIM_DIR, "animal")

        print(f"📊 Données trouvées : Langue={langue}, Animaux={animaux[:20]}...", flush=True)

        # 3. MISE À JOUR DYNAMODB
        # On utilise 'update_item' pour ne pas écraser les autres données déjà présentes
        table.update_item(
            Key={'video_id': video_uuid},
            UpdateExpression="set s3_url=:u, langue_detectee=:l, transcription_texte=:t, animaux_detectes=:a, #st=:s",
            ExpressionAttributeValues={
                ':u': s3_url,
                ':l': langue if langue else "Inconnue",
                ':t': texte if texte else "Texte non généré",
                ':a': animaux if animaux else "Aucun animal détecté",
                ':s': 'TERMINE'
            },
            ExpressionAttributeNames={
                "#st": "status" # 'status' est un mot réservé dans DynamoDB
            }
        )
        
        print(f"✅ BASE DE DONNÉES MISE À JOUR !", flush=True)
        return True

    except Exception as e:
        print(f"❌ Erreur transfert : {e}", flush=True)
        return False

def main():
    print("📡 TransfertData: Surveillance de 'videos_finales'...", flush=True)
    os.makedirs(FINAL_DIR, exist_ok=True)
    processed_files = set()

    while True:
        if os.path.exists(FINAL_DIR):
            files = os.listdir(FINAL_DIR)
            for file in files:
                if file.endswith(".mp4"):
                    if file not in processed_files:
                        time.sleep(1) 
                        if upload_and_index(file):
                            processed_files.add(file)
        time.sleep(5)

if __name__ == "__main__":
    main()