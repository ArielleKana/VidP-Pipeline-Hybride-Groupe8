import os
import time
import re

# --- CONFIGURATION ---
BASE_DIR = "/project/data"
# On surveille le dossier où subtitles.py dépose les fichiers textes
INPUT_DIR = os.path.join(BASE_DIR, "sous_titres") 
OUTPUT_DIR = os.path.join(BASE_DIR, "animaux_detectes")


def analyze_text_for_animals(input_path, output_path):
    """Analyse le texte et crée le dossier de sortie si besoin"""
    
    # --- SÉCURITÉ : Créer le dossier 'animaux_detectes' ---
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    # ----------------------------------------------------

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            texte = f.read().lower()
            
        # Ta liste d'animaux à chercher
        animaux_presents = []
        liste_animaux = ["éléphant", "gorille", "ours", "tigre", "rhinocéros", "loup", "lion", "chat", "chien", "chiot", "aigle",
    "oiseau", "perroquet", "chimpanzé",
    "girafe", "zèbre", "cheval", "poule", "coq", "vache", "taureau",
    "mouton", "chèvre", "cochon", "lapin", "serpent", "tortue", "poisson",
    "requin", "baleine", "dauphin", "crocodile", "insecte", "souris", "panda"
    "abeille", "fourmi", "araignée", "papillon", "cat", "dog", "bird", "poussin"
    "wolf", "bear", "monkey", "elephant", "zebra", "horse", "cow", "pig", "poussins","Vache","Veau","Cheval","Chien de berger",
    "Poussins","Lapin","Aigle","Perroquet","Lion","Girafe","Zèbre","Renard",
        "Serpent", "buffle", "méduse", "dragon de komodo", "Cat", "Dog", "Cow", "Calf", "Horse", "Foal",
        "Sheep", "Sheepdog", "Goat", "Pig", "Hen",
        "Rooster", "Chicks", "Duck", "Rabbit", "Bird",
        "Eagle", "Parrot","Tiger", "Elephant",
        "Giraffe", "Zebra", "Bear", "Wolf", "Fox",
        "Deer", "Snake", "Turtle", "Monkey", "Buffalo",
        "Jellyfish", "Hippopotamus", "Komodo Dragon",
         "Chat",
        "Chien",
        "Poulain",
        "Mouton",
        "Chèvre",
        "Cochon",
        "Poule",
        "Coq",
        "Canard",
        "Oiseau",
        "Éléphant",
        "Loup",
        "Cerf",
        "Tortue", "singe", "hippopotame","No animals detected", "No animals detected"]
        
        for animal in liste_animaux:
            if animal in texte:
                animaux_presents.append(animal)

        with open(output_path, "w", encoding="utf-8") as f:
            if animaux_presents:
                f.write(f"Animaux détectés : {', '.join(animaux_presents)}")
            else:
                f.write("Aucun animal détecté.")
        
        print(f"✅ Analyse terminée : {output_path}")
        return True
    except Exception as e:
        print(f"❌ Erreur lecture texte : {e}")
        return False

def main():
    print("👀 AnimalDetect (Mode Sémantique): Surveillance des textes...", flush=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    while True:
        if os.path.exists(INPUT_DIR):
            files = os.listdir(INPUT_DIR)
            
            for file in files:
                # On ne traite que les fichiers de sous-titres texte
                if file.endswith("_subtitles.txt"):
                    text_path = os.path.join(INPUT_DIR, file)
                    
                    # CORRECTION DU NOM : 
                    # On prend "nom_video_360p" et on ajoute "_animals.txt"
                    clean_name = file.replace("_subtitles.txt", "")
                    output_filename = f"{clean_name}_animals.txt"
                    
                    final_output_path = os.path.join(OUTPUT_DIR, output_filename)
                    
                    if not os.path.exists(final_output_path):
                        print(f"--------------------------------------------------")
                        print(f"📖 Lecture du texte : {file}")
                        # On passe text_path (source) et final_output_path (destination)
                        analyze_text_for_animals(text_path, final_output_path)

        time.sleep(2)

if __name__ == "__main__":
    main()