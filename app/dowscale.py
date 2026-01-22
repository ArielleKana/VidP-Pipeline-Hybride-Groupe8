import os
import time
import subprocess

# --- CONFIGURATION ---
BASE_DIR = "/project/data"
INPUT_DIR = os.path.join(BASE_DIR, "videos_originales")
OUTPUT_DIR = os.path.join(BASE_DIR, "videos_360p")
def downscale_video(input_path, output_path):
    """Convertit avec vérification de sécurité du dossier"""
    
    # --- SÉCURITÉ : On s'assure que le dossier de destination existe ---
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Dossier créé : {output_dir}")
    # ------------------------------------------------------------------

    temp_path = output_path + ".tmp"
    
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-i", input_path,
        "-vf", "scale=-2:360",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-c:a", "copy",
        "-f", "mp4", 
        temp_path
    ]
    
    try:
        print(f"📉 Conversion en cours : {os.path.basename(input_path)}...", flush=True)
        subprocess.run(cmd, check=True)
        os.rename(temp_path, output_path)
        print(f"✅ Conversion terminée : {output_path}", flush=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur FFmpeg : {e}", flush=True)
        if os.path.exists(temp_path):
            os.remove(temp_path) 
        return False

def main():
    print("👀 Dowscale (Mode Atomique): Prêt...", flush=True)
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    while True:
        if os.path.exists(INPUT_DIR):
            files = os.listdir(INPUT_DIR)
            
            for file in files:
                if file.endswith(".mp4"):
                    input_path = os.path.join(INPUT_DIR, file)
                    output_filename = file.replace(".mp4", "_360p.mp4")
                    output_path = os.path.join(OUTPUT_DIR, output_filename)
                    
                    # On ne traite que si le fichier final n'existe pas encore
                    if not os.path.exists(output_path):
                        print(f"--------------------------------------------------")
                        print(f"🎥 Nouvelle source détectée : {file}")
                        downscale_video(input_path, output_path)

        time.sleep(2)

if __name__ == "__main__":
    main()