import os
import time
import subprocess
import speech_recognition as sr
from datetime import timedelta

# --- CONFIGURATION ---
BASE_DIR = "/project/data"
INPUT_DIR = os.path.join(BASE_DIR, "videos_360p")
SUBTITLE_DIR = os.path.join(BASE_DIR, "sous_titres")
OUTPUT_DIR = os.path.join(BASE_DIR, "videos_finales")
LANG_DIR = os.path.join(BASE_DIR, "languages_detected") # AJOUT

# Création des dossiers
for d in [SUBTITLE_DIR, OUTPUT_DIR, LANG_DIR]:
    os.makedirs(d, exist_ok=True)

def format_timestamp(seconds):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def extract_audio(video_path, audio_path):
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", video_path, "-vn", 
           "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path]
    subprocess.run(cmd, check=True)

def generate_real_subtitles(video_path, srt_path, lang_path):
    audio_path = video_path + ".wav"
    txt_path = srt_path.replace(".srt", "_subtitles.txt")
    recognizer = sr.Recognizer()
    full_text = []
    
    try:
        extract_audio(video_path, audio_path)
        print(f"👂 Analyse vocale (Google API) en cours...", flush=True)
        
        srt_content = ""
        block_duration = 10 
        
        with sr.AudioFile(audio_path) as source:
            duration = int(source.DURATION)
            for i, chunk_start in enumerate(range(0, duration, block_duration)):
                audio_data = recognizer.record(source, duration=block_duration)
                try:
                    text = recognizer.recognize_google(audio_data, language="fr-FR")
                    start_time = format_timestamp(chunk_start)
                    end_time = format_timestamp(chunk_start + block_duration)
                    srt_content += f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n"
                    full_text.append(text)
                    print(f"   🗣️ Entendu : '{text}'", flush=True)
                except:
                    pass

        # 1. Sauvegarde SRT (Correction de l'erreur Directory)
        try:
            os.makedirs(os.path.dirname(srt_path), exist_ok=True) # Force la création du dossier
            with open(srt_path, "w", encoding="utf-8") as f:
                if not srt_content:
                    srt_content = "1\n00:00:00,000 --> 00:00:05,000\n(Silence)\n\n"
                f.write(srt_content)
            print(f"✅ Fichier SRT écrit avec succès", flush=True)
        except Exception as e:
            print(f"⚠️ Erreur écriture SRT : {e}", flush=True)

        # 2. Sauvegarde TXT
        txt_path = srt_path.replace(".srt", "_subtitles.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(" ".join(full_text))

        # 3. Sauvegarde LANGUE (On force 'fr' car Google a utilisé 'fr-FR')
        lang_path = os.path.join(LANG_DIR, os.path.basename(video_path) + "_langue.txt")
        with open(lang_path, "w", encoding="utf-8") as f:
            f.write("fr")

        return True
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False
    finally:
        if os.path.exists(audio_path): os.remove(audio_path)

def burn_subtitles(video_input, srt_input, video_output):
    # Utilisation d'un chemin simplifié pour FFmpeg
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-i", video_input,
        "-vf", f"subtitles={srt_input}",
        "-c:a", "copy",
        video_output
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Vidéo finale prête : {video_output}")
        return True
    except:
        print(f"❌ Erreur FFmpeg")
        return False

def main():
    print("👀 Subtitles: Prêt...", flush=True)
    while True:
        if os.path.exists(INPUT_DIR):
            for file in os.listdir(INPUT_DIR):
                if file.endswith("_360p.mp4"):
                    input_path = os.path.join(INPUT_DIR, file)
                    srt_path = os.path.join(SUBTITLE_DIR, f"{file}.srt")
                    lang_path = os.path.join(LANG_DIR, f"{file}_langue.txt")
                    final_output = os.path.join(OUTPUT_DIR, file.replace('.mp4', '_subtitled.mp4'))
                    
                    if not os.path.exists(final_output):
                        print(f"--- Nouveau traitement : {file} ---")
                        if generate_real_subtitles(input_path, srt_path, lang_path):
                            burn_subtitles(input_path, srt_path, final_output)
        time.sleep(5)

if __name__ == "__main__":
    main()